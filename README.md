# Information Retrieval: Sweets Search Engine

## Presentation
Project_Presentation.pptx

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
| co  | "flat" or "single"  or "average" | This is the selected clustering option selected in the front end UI  |  
| qe  | "association" or "metric" or "scalar" | This is the selected query expansion option selected in the front end UI   |  






