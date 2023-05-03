from pysolr import Solr
from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from clustering import Clustering
from urllib.parse import urlparse
import QE
import random

import nltk
from nltk.corpus import stopwords
import string
stop_words = set(stopwords.words("english"))

def query_preprocess(query):
    words = nltk.word_tokenize(query)
    preprocess_words = [word.lower() for word in words if word.lower() not in stop_words and word not in string.punctuation]
    return ' '.join(preprocess_words)

app = Flask(__name__)
app.config["DEBUG"] = True
CORS(app)

solr_url_local = 'http://localhost:8983/solr/nutch'
solr_url_ec2 = 'http://ec2-44-195-249-49.compute-1.amazonaws.com:8983/solr/nutch'

solr = Solr(solr_url_local, always_commit=True)

cluster = Clustering()

qe=''

@app.route('/api', methods=['GET'])
def main():
    solr_query = '*'

    if 'query' in request.args:
        query = (request.args['query']).lower()
        preprocess_query = query_preprocess(query)
        if(query[0] == "\""):
            solr_query = 'text:' + preprocess_query
        else:
            solr_query = "text:" + "\"" + preprocess_query + "\""

    


    rm =  request.args['rm'] if 'rm' in request.args else ''
    co =  request.args['co'] if 'co' in request.args else ''
    qe =  request.args['qe'] if 'qe' in request.args else ''
    
    solr_results = get_results_from_solr(solr_query,qe)

    if(len(rm) != 0):
        solr_results = get_relevance_model_results(rm, solr_results)
    if(len(co) != 0):
        solr_results = get_clustering_result(preprocess_query, co, solr_results)
    if(len(qe) != 0):
        new_query, solr_results = get_query_expansion_result(preprocess_query, qe, solr_results,query)

    results = {}
    results['query'] = query if len(qe) == 0 else new_query
    results['query_results'] = solr_results
    return jsonify(results)

def get_domain(url):
    return urlparse(url).netloc

def randomize_result(results):
    batch_size = 10
    new_results = results[:2]

    for idx in range(2, len(results), batch_size):
        data = results[idx: idx + batch_size]
        random.shuffle(data)
        new_results.extend(data)

    return new_results

def get_filter_query(results):
    new_results = []
    elements = {}
    looked_urls = set()
    for res in results:
        if res['url'] != '' and res['url'] not in looked_urls:
            domain = get_domain(res['url'])
            if domain in elements and elements[domain] < 4:
                new_results.append(res)
                elements[domain] += 1
            elif domain not in elements:
                elements[domain] = 1
                new_results.append(res)
            looked_urls.add(res['url'])

    return new_results

def get_results_from_solr(query,qe=''):
    num_rows = 200
    curr_count = 0
    print("Query: ",query)
    while curr_count < 50:
        solr_response = solr.search(query, search_handler="/select", **{
            "wt": "json",
            "rows": num_rows
        })
        solr_results = [result for result in solr_response]

        if num_rows > 10000:
            return randomize_result(solr_results)
        if len(solr_results) < 50:
            queries = (query.split(":")[1]).split()
            and_search_query = ""
            or_search_query = ""
            for new_query in queries[:-1]:
                if new_query[0] == '\"':
                    new_query = "".join(list(new_query)[1:])

                if new_query[-1] == '\"':
                    new_query = "".join(list(new_query)[:-1])

                and_search_query += "text:" + new_query + " AND "
                or_search_query += "text:" + new_query + " OR "

            new_query = queries[-1]
            if new_query[-1] == '\"':
                new_query = "".join(list(new_query[:-1]))

            and_search_query += "text:" + new_query
            or_search_query += "text:" + new_query
            # print(f"AND Search Query: {and_search_query}")
            # print(f"OR Search Query: {or_search_query}")

            solr_response = solr.search(and_search_query, search_handler="/select", **{
                "wt": "json",
                "rows": num_rows
            })
            solr_results = [result for result in solr_response]
            # print(f"Result length of AND: {len(solr_results)}")
            solr_response = solr.search(or_search_query, search_handler="/select", **{
                "wt": "json",
                "rows": num_rows
            })
            temp = [result for result in solr_response]
            # print(f"Result length of OR: {len(temp)}")
            solr_results.extend(temp)
            filter_result = get_filter_query(solr_results)
            # print(f"Final results size: {len(filter_result)}")
            #return filter_result

        solr_results = get_filter_query(solr_results)

        curr_count = len(solr_results)
        print(f"Curr Count: {curr_count}")
        num_rows *= 2
    #return randomize_result(solr_results)
    print(qe)
    if qe != '':
        return solr_results
    return randomize_result(solr_results) 



def get_relevance_model_results(rm, solr_results):
    rm = rm.replace('"', '')
    if rm == "page_rank":
        return solr_results
    else:
        return get_page_rank_results(solr_results)

def get_page_rank_results(solr_results):
    page_rank_dict = {}

    with open('results/pr_modified_scores.txt', 'r') as file:
            page_rank_dict = json.load(file)

    return sorted(solr_results, key=lambda x: page_rank_dict.get(x['url'], 0), reverse=True)

def get_hits_rank_results(solr_results):
    hits_rank_dict = {}

    with open('results/hits_scores.txt', 'r') as file:
        hits_rank_dict = json.load(file)

    return sorted(solr_results, key=lambda x: hits_rank_dict.get(x['url'], 0), reverse=True)

def get_clustering_result(query, clustering_type, solr_results):
    clustering_type = clustering_type.replace('"', '')

    if clustering_type == "flat":
        return cluster.flat_Clustering(query, solr_results)
    elif clustering_type == 'single':
        return cluster.hierarchical_clustering_single(query, solr_results)
    else:
        return cluster.hierarchical_clustering_average(query, solr_results)

def get_query_expansion_result(query, query_expansion_type, solr_results,original_query):
    query = query.replace('"', '')
    query_expansion_type = query_expansion_type.replace('"', '')
    expanded_query=""
    if query_expansion_type == "association":
        expanded_query = original_query+QE.association_main(query, solr_results[:20],3,10)
    elif query_expansion_type == "metric": 
        expanded_query = original_query+QE.association_main(query, solr_results[:30],6,14)
    elif query_expansion_type == "scalar": 
        expanded_query = original_query+QE.association_main(query, solr_results[:30],12,15)
    #print(expanded_query)
    expanded_query = " ".join(expanded_query.split())
    #Remove duplicates
    words = expanded_query.split()
    unique_words = list(dict.fromkeys(words))
    expanded_query = " ".join(unique_words)
    expanded_query = '"'+expanded_query+'"'
    # #print(f"qet: {expanded_query}")
    # exp_quer = expanded_query.split()
    # #print(exp_quer)
    # exp_quer_result=''
    # for i in range(0,len(exp_quer)):
    #     exp_quer_result = exp_quer_result+exp_quer[i]
    #     if(i<1):
    #         exp_quer_result = exp_quer_result+' '
    #     if(i==1):
    #         break
    # exp_quer_result = exp_quer_result.replace('"', '')
    # exp_quer_result = '"'+exp_quer_result+'"'
    #print("heres the "+original_query)
    results_from_solr = get_results_from_solr('text:'+expanded_query)
    # if(original_query.lower()!='desserts of texas'):
    #     results_from_solr = get_results_from_solr('text:'+expanded_query)
    # else:
    #     words_exp = expanded_query.split()   # split the string into words
    #     new_string = ' '.join(words_exp[3:])
    #     results_from_solr = get_results_from_solr('text:'+new_string)
    #print(expanded_query)
    #print(results_from_solr)
    return expanded_query, results_from_solr

app.run()