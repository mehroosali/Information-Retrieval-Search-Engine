from pysolr import Solr
from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from clustering import Clustering
from urllib.parse import urlparse

app = Flask(__name__)
app.config["DEBUG"] = True
CORS(app)

solr_url_local = 'http://localhost:8983/solr/nutch'
solr_url_ec2 = 'http://ec2-54-152-69-118.compute-1.amazonaws.com:8983/solr/nutch'

solr = Solr(solr_url_ec2, always_commit=True)

cluster = Clustering()

@app.route('/api', methods=['GET'])
def main():
    solr_query = '*'

    if 'query' in request.args:
        query = request.args['query']
        solr_query = 'text:' + query

    solr_results = get_results_from_solr(solr_query)

    rm =  request.args['rm'] if 'rm' in request.args else ''
    co =  request.args['co'] if 'co' in request.args else ''
    qe =  request.args['qe'] if 'qe' in request.args else ''

    if(len(rm) != 0):
        solr_results = get_relevance_model_results(rm, solr_results)
    if(len(co) != 0):
        solr_results = get_clustering_result(query, co, solr_results)

    return jsonify(solr_results)

def get_domain(url):
    return urlparse(url).netloc

def get_results_from_solr(query):
    num_rows = 50
    curr_count = 0

    while curr_count < 50:
        solr_response = solr.search(query, search_handler="/select", **{
            "wt": "json",
            "rows": num_rows
        })
        solr_results = [result for result in solr_response]

        if len(solr_results) < 50:
            return solr_results
        
        elements = {}
        new_results = []
        for res in solr_results:
            if res['url'] != '':
                domain = get_domain(res['url'])
                if domain in elements and elements[domain] < 4:
                    new_results.append(res)
                    elements[domain] += 1
                elif domain not in elements:
                    elements[domain] = 1
                    new_results.append(res)
        curr_count = len(new_results)
        print(f"Curr Count: {curr_count}")

        if curr_count >= 50:
            return new_results[:50]
        
        num_rows *= 2

    return solr_results

def get_relevance_model_results(rm, solr_results):
    rm = rm.replace('"', '')

    if rm == "page_rank":
        return get_page_rank_results(solr_results)
    else:
        return get_hits_rank_results(solr_results)

def get_page_rank_results(solr_results):
    page_rank_dict = {}

    with open('results/page_rank_scores.txt', 'r') as file:
        for line in file:
            line_arr = line.split('\t')
            url, score = line_arr[0], float(line_arr[1].strip())
            page_rank_dict[url] = score

    return sorted(solr_results, key=lambda x: page_rank_dict.get(x['url'], 0))

def get_hits_rank_results(solr_results):
    hits_rank_dict = {}

    with open('results/authorities_scores.txt', 'r') as file:
        hits_rank_dict = json.load(file)

    return sorted(solr_results, key=lambda x: hits_rank_dict.get(x['url'], 0))

def get_clustering_result(query, clustering_type, solr_results):
    clustering_type = clustering_type.replace('"', '')

    if clustering_type == "flat":
        return cluster.flat_Clustering(query, solr_results)
    else:
        return cluster.hierarchical_clustering(query, solr_results)
    
app.run()