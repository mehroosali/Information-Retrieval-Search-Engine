import "./App.css";
import React, { useState } from "react";
import axios from "axios";
import "./styles.css";

const api_url = "http://localhost:5000/api";

function App() {
  document.title = "Search Engine";
  const [text, setText] = useState("");
  const [data, setData] = useState([]);
  const [relevanceOption, setRelevanceOption] = useState("");
  const [clusteringOption, setClusteringOption] = useState("");
  const [queryExpOption, setQueryExpOption] = useState("");

  

  const getResponseFromApi = (event) => {
    if (event.key === "Enter") {
      console.log("inside getResponseFromApi");

      axios
        .get(api_url, {
          params: {
            query: text,
          },
        })
        .then((response) => setData(response.data.slice(0, 25)));
    }
  };

  const handleSearch = (event) => {
    event.preventDefault();
    
    const input = document.getElementById("UserInput").value;

    // Build the URLs for Google and Bing search
    const googleUrl =
      "https://www.google.com/search?igu=1&source=hp&ei=lheWXriYJ4PktQXN-LPgDA&q=" +
      input;
    const bingUrl = "https://www.bing.com/search?q=" + input;
    console.log("inside handleSearch");

    // Set the URLs as the sources for the iframes
    document.getElementById("google").src = googleUrl;
    document.getElementById("bing").src = bingUrl;
    // Call the API to get the search results
    let params = {
      query: text,
    };
  
    if (relevanceOption === "page_rank") {
      params.rm = "page_rank";
    } else if (relevanceOption === "hits") {
      params.rm = "hits";
    }
  
    if (clusteringOption === "flat_clustering") {
      params.co = "flat";
    } else if (clusteringOption === "hierarchical_clustering") {
      params.co = "hierarchical";
    }

    if (queryExpOption === "association_qe") {
      params.qe = "association";
    } else if (queryExpOption === "scalar_qe") {
      params.qe = "scalar";
    } else if (queryExpOption==="metric_qe"){
      params.qe="metric"
    }
    console.log("below are the params")
    console.log(params)
    axios
      .get(api_url, { params })
      .then((response) => setData(response.data.slice(0, 25)));
  };

  return (
    <div className="App">
      <h1>Sweets Search Engine</h1>
      <form id="form" onSubmit={handleSearch}>
        <input
          className="search-box"
          type="text"
          placeholder="Enter query here..."
          id="UserInput"
          value={text}
          onChange={(e) => setText(e.target.value)}
          onKeyDown={(e) => getResponseFromApi(e)}
        />
        <br />
        <div className="options">
          <p className="result-title" id="relevance">
            Relevance Model Options:
          </p>
          <input
            type="radio"
            // checked
            id="page_rank"
            name="rm"
            value="page_rank"
            checked={relevanceOption === "page_rank"}
            onChange={(e) => setRelevanceOption(e.target.value)}
          />
          <label id="page_rank_label" htmlFor="page_rank">
            Page Rank
          </label>
          <input
            type="radio"
            id="hits"
            name="rm"
            value="hits"
            className="margin"
            checked={relevanceOption === "hits"}
            onChange={(e) => setRelevanceOption(e.target.value)}
          />
          <label id="hits_label" htmlFor="hits">
            HITS
          </label>
        </div>

        <div className="options">
          <p id="clustering" className="result-title">
            Clustering Options:
          </p>
          <input
            type="radio"
            id="flat_clustering"
            name="co"
            value="flat_clustering"
            checked={clusteringOption === "flat_clustering"}
            onChange={(e) => setClusteringOption(e.target.value)}
          />
          <label id="flat_clustering_label" htmlFor="flat_clustering">
            Flat Clustering
          </label>
          <input
            type="radio"
            id="hierarchical_clustering"
            name="co"
            value="hierarchical_clustering"
            className="margin"
            checked={clusteringOption === "hierarchical_clustering"}
            onChange={(e) => setClusteringOption(e.target.value)}
          />
          <label
            id="hierarchical_clustering_label"
            htmlFor="hierarchical_clustering"
          >
            Hierarchical Clustering
          </label>
        </div>

        <div className="options">
          <p id="queryexp" className="result-title">
            Query Expansion Option:
          </p>
          <input
            type="radio"
            id="association_qe"
            name="qe"
            value="association_qe"
            checked={queryExpOption === "association_qe"}
            onChange={(e) => setQueryExpOption(e.target.value)}
          />
          <label id="association_qe_label" htmlFor="association_qe">
            Association
          </label>
          <input type="radio" id="metric_qe" name="qe" value="metric_qe" checked={queryExpOption === "metric_qe"}
            onChange={(e) => setQueryExpOption(e.target.value)}/>
          <label id="metric_qe_label" htmlFor="metric_qe">
            Metric
          </label>
          <input type="radio" id="scalar_qe" name="qe" value="scalar_qe" checked={queryExpOption === "scalar_qe"}
            onChange={(e) => setQueryExpOption(e.target.value)}/>
          <label id="scalar_qe_label" htmlFor="scalar_qe">
            Scalar
          </label>
        </div>
        <br />
        <hr />
        <input
          id="srch"
          type="submit"
          // value="Search"
          value="Search"
          onSubmit={(e) => handleSearch(e)}
        />
        <hr />
      </form>

      {/* data && data.map((item) => <p>{item.title}</p>) */}
      <div className="container">
        {data.map((item) => (
          <div className="card" key={item.id}>
            <h2 className="card-title">{item.title}</h2>
            <p className="card-content">{item.content}</p>
            <a
              className="card-link"
              href={item.url}
              target="_blank"
              rel="noreferrer"
            >
              Read more
            </a>
          </div>
        ))}
      </div>
      <iframe
        id="google"
        title="Google search results"
        src="https://www.google.com"
      ></iframe>
      <iframe
        id="bing"
        title="Bing search results"
        src="https://www.bing.com/search?q="
      ></iframe>
    </div>
  );
}

export default App;
