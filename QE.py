
import re
import collections
import heapq
import sklearn

import numpy as np
from nltk.corpus import stopwords
from nltk import PorterStemmer
import pysolr
import pprint

class Element:

    def __init__(self, u, v, value):
        self.u = u
        self.v = v
        self.value = value

    def __lt__(self, other):
        return self.value < other.value

    def __le__(self, obj):
        """self <= obj."""
        return self.value <= obj.value

    def __eq__(self, obj):
        """self == obj."""
        if not isinstance(obj, Element):
            return False
        return self.value == obj.value

    def __ne__(self, obj):
        """self != obj."""
        if not isinstance(obj, Element):
            return True
        return self.value != obj.value

    def __gt__(self, obj):
        """self > obj."""
        return self.value > obj.value

    def __ge__(self, obj):
        """self >= obj."""
        return self.value >= obj.value

    def __repr__(self):
        return '<Element(u="{}", v="{}", value=("{}"))>'.format(self.u, self.v, self.value)


# def get_results_from_solr(query, solr):
#     results = solr.search('text: "'+query+'"', search_handler="/select", **{
#         "wt": "json",
#         "rows": 50
#     })
#     return results


# def __init__(self):
#     self.metric_cluster_main(query='')
#     self.scalar_main(query='')
#     self.association_main(query='')
# returns a list of tokens

def tokenize_doc(doc_text, stop_words):
    # doc_text = doc_text.replace('\n', ' ')
    # doc_text = " ".join(re.findall('[a-zA-Z]+', doc_text))
    # tokens = doc_text.split(' ')
    tokens = []
    text = doc_text
    text = re.sub(r'[\n]', ' ', text)
    text = re.sub(r'[,-]', ' ', text)
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub('[0-9]', '', text)
    text = text.lower()
    tkns = text.split(' ')
    tokens = [token for token in tkns if token not in stop_words and token != '' and not token.isnumeric()]
    return tokens

def build_association(id_token_map, vocab, query):
    association_list = []
    # print(id_token_map)
    # print(vocab)
    for i, voc in enumerate(vocab):
        for word in query.split(' '):
            c1, c2, c3 = 0, 0, 0
            for doc_id, tokens_this_doc in id_token_map.items():
                count0 = tokens_this_doc.count(voc)
                count1 = tokens_this_doc.count(word)
                c1 += count0 * count1
                c2 += count0 * count0
                c3 += count1 * count1
            c1 /= (c1 + c2 + c3)
            if c1 != 0:
                association_list.append((voc, word, c1))
                #print(association_list)


    return association_list

    
def association_main(query, solr_results):
    stop_words = set(stopwords.words('english'))
    #query = 'blueberry milkshake'
    #solr = pysolr.Solr('http://ec2-54-152-69-118.compute-1.amazonaws.com:8983/solr/nutch', always_commit=True, timeout=10)
    results = solr_results
    tokens = []
    token_counts = {}
    tokens_map = {}
    # tokens_map = collections.OrderedDict()
    document_ids = []
    for result in results:
        tokens_this_document = tokenize_doc(result['content'], stop_words)
        tokens_map[result['digest']] = tokens_this_document
        tokens.append(tokens_this_document)

    vocab = set([token for tokens_this_doc in tokens for token in tokens_this_doc])
    #print('Vocab len ', len(vocab))
    #print('Tokens Map len ', len(tokens_map))
    association_list = build_association(tokens_map, vocab, query)
    association_list.sort(key = lambda x: x[2],reverse=True)
    #print(association_list)

    i=0
    while(i<2):
        query += ' '+str(association_list[i][0])
        i +=1
    #print(query)
    return query

def make_stem_map(tokens):
    porter_stemmer = PorterStemmer()
    stem_map = {}
    for tokens_this_document in tokens:
        for token in tokens_this_document:
            stem = porter_stemmer.stem(token)
            if stem not in stem_map:
                stem_map[stem] = set()
            stem_map[stem].add(token)
    return stem_map

def print_top_n(normalized_matrix, stems, query, tokens_map, stem_map, top_n=3):
    query = query.lower()
    strings = set()
    for string in query.split(' '):
        strings.add(string)
    elements = np.zeros((len(strings), top_n)).tolist()
    index = 0
    queue = []
    for string in strings:
        queue = []
        i = -1
        porter_stemmer = PorterStemmer()

        if porter_stemmer.stem(string) in stems:
            i = list(stems).index(porter_stemmer.stem(string))

        if i==-1:
            #print('continuing')
            continue

        for j in range(len(normalized_matrix[i])):
            if normalized_matrix[i][j] == 0 \
                or (normalized_matrix[i][j].u in strings and normalized_matrix[i][j].u != string) \
                or (normalized_matrix[i][j].v in strings and normalized_matrix[i][j].v != string):
                #print('continuing 2')
                continue

            if normalized_matrix[i][j].v in tokens_map:
                heapq.heappush(queue, normalized_matrix[i][j])

            else:
                heapq.heappush(queue, \
                    Element(normalized_matrix[i][j].u, \
                        next(iter( stem_map[ normalized_matrix[i][j].v ] )), \
                        normalized_matrix[i][j].value))

            if len(queue) > top_n:
                heapq.heappop(queue)

        for k in range(top_n):
            # for k in range(top_n):
            elements[index][k] = heapq.heappop(queue)
        index+=1
        #print('index', index)

    return elements

def get_metric_clusters(tokens_map, stem_map, query):
    # matrix = [[]]
    # matrix is a 2-d array (square matrix) of size (len(stem_map.keys())) or len(stem_map)
    matrix = np.zeros((len(stem_map), len(stem_map))).tolist()
    stems = stem_map.keys()
    for i, stem_i in enumerate(stems):
        for j, stem_j in enumerate(stems):
            if i==j:
                continue
            
            cuv = 0.0
            i_strings = stem_map[stem_i]
            j_strings = stem_map[stem_j]

            for string1 in i_strings:
                for string2 in j_strings:
                    i_map = tokens_map[string1]
                    j_map = tokens_map[string2]
                    for document_id in i_map:
                        if document_id in j_map:
                            if i_map[document_id] - j_map[document_id] != 0:
                                cuv += 1 / abs( i_map[document_id] - j_map[document_id] )

            matrix[i][j] = Element(stem_i, stem_j, cuv)

    normalized_matrix = np.zeros((len(stem_map), len(stem_map))).tolist()

    for i, stem_i in enumerate(stems):
        for j, stem_j in enumerate(stems):
            if i==j:
                continue

            cuv = 0.0
            if matrix[i][j] != 0:
                cuv = matrix[i][j].value / ( len(stem_map[stem_i]) * len(stem_map[stem_j]) )

            normalized_matrix[i][j] = Element(stem_i, stem_j, cuv)

    # print(normalized_matrix.shape())
    # pprint.pprint(normalized_matrix)
    return print_top_n(normalized_matrix, stems, query, tokens_map, stem_map, top_n=3)
    # pass


def metric_cluster_main(query, solr_results=[]):
    stop_words = set(stopwords.words('english'))
    #query = 'popsicles'
    #solr = pysolr.Solr('http://ec2-54-152-69-118.compute-1.amazonaws.com:8983/solr/nutch', always_commit=True, timeout=10)
    #results = get_results_from_solr(query, solr)
    # with open('C:/Users/minal/.spyder-py3/All_Documents.json',encoding="utf8") as file:
    #     results = json.load(file)
    #results = results['response']['docs']
    tokens = []
    token_counts = {}
    tokens_map = {}
    # tokens_map = collections.OrderedDict()
    document_ids = []

    for result in solr_results:
        
        document_id = result['digest']
        document_ids.append(document_id)
        tokens_this_document = tokenize_doc(result['content'], stop_words)
        token_counts = collections.Counter(tokens_this_document)
        for token in tokens_this_document:
            if token not in tokens_map:
                tokens_map[token] = {document_id: token_counts[token]}
            elif document_id not in tokens_map[token]:
                tokens_map[token][document_id] = token_counts[token]
            else:
                tokens_map[token][document_id] += token_counts[token]
        tokens.append(tokens_this_document)

    stem_map = make_stem_map(tokens)
    #print(tokens_map)
    metric_clusters = get_metric_clusters(tokens_map, stem_map, query)
    metric_clusters2 = [elem for cluster in metric_clusters for elem in cluster]
    metric_clusters2.sort(key=lambda x:x.value,reverse=True)
    i=0;
    while(i<1):
        query += ' '+ str(metric_clusters2[i].v)
        i+=1
    print(query)  
    return query

def Create_Scalar_Clustering(results, Query_String ):
    Query = Query_String.split(" ")
    #with open(json_file, encoding="utf8") as file:
    #   res = json.load(file)

    #docs = results['response']['docs']
    URL_Lists = []
    Documents_terms = []
    doc_dict = {}

    # for doc in docs:
    #     URL_Lists.append(doc['url'])

    for doc_no, doc in enumerate(results):
    #     Documents_List.append(doc['content'].replace("\n", " "))
        Documents_terms.extend(doc['content'].replace("\n", " ").split(" "))
        doc_dict[doc_no] = doc['content'].replace("\n", " ").split(" ")
    # Doc_Terms = list(set(Documents_terms))
    Doc_Terms = []
    for term in Documents_terms:
        if term not in Doc_Terms:
            Doc_Terms.append(term)

    # Creating a vocabulary
    # Query = ["Olympic", "Medal"]
    Vocab_dict = {}
    AllDoc_vector = np.zeros(len(Doc_Terms))
    for i, term in enumerate(Doc_Terms):
        Vocab_dict[i] = term
    from collections import Counter
    count_dict  = Counter(Documents_terms)

    Relevant_Docs=[]
    NonRelevant_Docs=[]
    count_relevant_docs = 30
    for i, doc in doc_dict.items():
        if i < count_relevant_docs:
            Relevant_Docs.append(doc)
        else:
            NonRelevant_Docs.append(doc)

    # Vector_Relevant
    AllDoc_vector = np.zeros(len(Doc_Terms))
    Vector_Relevant = []
    for docs in Relevant_Docs:
        rel_vec = np.zeros(len(Doc_Terms))
        for term in docs:
            count = docs.count(term) 
            rel_vec[Doc_Terms.index(term)] = count
        Vector_Relevant.append(rel_vec)

    M1 = np.array(Vector_Relevant)
    M1 = M1.transpose()
    Correlation_Matrix = np.matmul(M1, M1.transpose())
    shape_M = Correlation_Matrix.shape
    
    for i in range(shape_M[0]):
        for j in range(shape_M[1]):
            if Correlation_Matrix[i][j]!=0:
                Correlation_Matrix[i][j] =  Correlation_Matrix[i][j]/( Correlation_Matrix[i][j]+ Correlation_Matrix[i][i]+ Correlation_Matrix[j][j])
    # Correlation_Matrix        

    CM = Correlation_Matrix
    indices_query = []
    for q in Query:
        indices_query.append(Doc_Terms.index(q))
    # indices_query

    for i in indices_query:
        max_cos = 0
        max_index = 0
        for j in range(shape_M[1]):
            if i==j:
                continue
            cos = np.dot(CM[i], CM[j]) / (np.sqrt(np.dot(CM[i],CM[i])) * np.sqrt(np.dot(CM[j],CM[j])))
            if np.isnan(cos):
                continue

            # print(cos)
            if cos > max_cos:
                max_cos = cos
                max_index = j
        # print(max_cos)
        #Query.append(Doc_Terms[max_index]+" "+Doc_Terms[max_index-1]+" "+Doc_Terms[max_index-2])
        Query.append(Doc_Terms[max_index])
        # print("similar term for",Doc_Terms[i], "is:",  Doc_Terms[max_index])
    return " ".join(Query)
                



def scalar_main(query, solr_results=[]):
    # execute only if run as a script
    stop_words = set(stopwords.words('english'))
    #query = 'sherbet'
    #solr = pysolr.Solr('http://ec2-54-152-69-118.compute-1.amazonaws.com:8983/solr/nutch', always_commit=True, timeout=10)
    #results = get_results_from_solr(query, solr)
    tokens = []
    token_counts = {}
    tokens_map = {}
    #tokens_map = collections.OrderedDict()
    document_ids = []

    for result in solr_results:
        document_id = result['digest']
        document_ids.append(document_id)
        tokens_this_document = tokenize_doc(result['content'], stop_words)
        token_counts = collections.Counter(tokens_this_document)
        for token in tokens_this_document:
            if token not in tokens_map:
                tokens_map[token] = {document_id: token_counts[token]}
            elif document_id not in tokens_map[token]:
                tokens_map[token][document_id] = token_counts[token]
            else:
                tokens_map[token][document_id] += token_counts[token]
        tokens.append(tokens_this_document)


    #json_file  = r"All_Documents.json"
    #Query_String = "Olympic medal"
    Expanded_Query  = Create_Scalar_Clustering(solr_results, query)
    #print(Expanded_Query)
    return Expanded_Query

# def perform_QE(typeofQE,query):
#     if typeofQE == 'Association':
#         association_main(query)
#     elif typeofQE == 'Metric': 
#         metric_cluster_main(query)
#     elif typeofQE == 'Scalar': 
#         scalar_main(query)
    


# if __name__ == "__main__":
#     perform_QE('Association','cake')