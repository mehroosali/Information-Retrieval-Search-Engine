import pysolr
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
app.config["DEBUG"] = True
CORS(app)

solr_url_local = 'http://localhost:8983/solr/nutch'
solr_url_ec2 = 'http://ec2-54-152-69-118.compute-1.amazonaws.com:8983/solr/nutch'

solr = pysolr.Solr(solr_url_ec2, always_commit=True)

@app.route('/api', methods=['GET'])
def main():
    solr_query = '*'
    if 'query' in request.args:
        solr_query = 'text:'+request.args['query']

    solr_response = solr.search(solr_query, search_handler="/select", **{
        "wt": "json",
        "rows": 20
    })

    return jsonify([result for result in solr_response])

app.run()