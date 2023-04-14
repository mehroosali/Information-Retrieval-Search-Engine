# Information Retrieval: Sweets Search Engine

## Pending Tasks
- [ ] Task 5 (Query Expansion) code implementation and testing.
- [ ] Complete front end to backend integration and testing. 
- [ ] Complete final UI design.
- [ ] Fix method get_page_rank_results or get_hits_rank_results to get different results in page rank vs hits.  
- [ ] Complete Project Report (All tasks).
- [ ] Final integration testing with pre selected queries for demo.

## Project Drive
 https://drive.google.com/drive/folders/16sr1Bx4XxMW5sMc1wH3C-0Pim_O97-P4?usp=sharing
 
## Prerequisites

- [NodeJS](https://nodejs.org/)
- [Python](https://www.python.org/)
- [Flask](https://pypi.org/project/Flask/)
- [Flask Cors](https://pypi.org/project/Flask-Cors/)
- [PySolr](https://pypi.org/project/pysolr/)
- [Postman](https://www.postman.com/downloads/)


## Setup

In the project directory, run the following to install flask, flask_cors, pysolr, react:

### `npm install`
### `pip install pysolr`
### `pip install flask`
### `pip install flask_cors`

To run the backend code:
### `python backend.py`

To run the frontend code:
### `npm start`

React UI: http://localhost:3000 <br>
Backend API: http://localhost:5000/api <br>

## API Testing

Install Postman to test backend API.

API Params:

|  key | value  |  description | 
|---|---|---|
| query | e.g. "Chocolate Cake"  | This is the query string coming from front end UI which is used to query Solr to retrieve documents | 
| rm  | "page_rank" or "hits"  |  This is the selected relevance model option selected in the front end UI|  
| co  | "flat" or "agglomerative"  | This is the selected clustering option selected in the front end UI  |  
| qe  | "association" or "metric" or "scalar" | This is the selected query expansion option selected in the front end UI   |  






