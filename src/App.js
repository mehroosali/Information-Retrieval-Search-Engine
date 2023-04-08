import "./App.css";
import React, { useState } from "react";
import axios from "axios";
import "./styles.css";

const api_url = "http://localhost:5000/api";

function App() {
  document.title = "Search Engine";
  const [text, setText] = useState("");
  const [data, setData] = useState([]);

  const dummydata = [
    {
      tstamp: "2023-03-05T02:34:43.119Z",
      digest: "3eadbda6b298dc05f5aa4162fc5cfc58",
      boost: 1.0,
      id: "https://bakesbybrownsugar.com/category/desserts/",
      title: "Delicious Dessert Recipes - Bakes by Brown Sugar",
      url: "https://bakesbybrownsugar.com/category/desserts/",
      content: "Delicious Dessert Recipes - Bakes by Brown Sugar\n",
      _version_: 1759493524310458368,
    },
    {
      tstamp: "2023-03-05T02:34:42.825Z",
      digest: "0839a9fdae6d8c1e65e3526c1efa0430",
      boost: 1.0,
      id: "https://butteryourbiscuit.com/category/dessert/",
      title: "Dessert - Butter Your Biscuit",
      url: "https://butteryourbiscuit.com/category/dessert/",
      content: "Dessert - Butter Your Biscuit\n",
      _version_: 1759493524312555520,
    },
    {
      tstamp: "2023-03-05T02:34:43.126Z",
      digest: "acb41c8c8efc3b25d8906f73c58c666b",
      boost: 1.0,
      id: "https://celebratingsweets.com/recipe-index/",
      title: "Recipe Index - Celebrating Sweets",
      url: "https://celebratingsweets.com/recipe-index/",
      content: "Recipe Index - Celebrating Sweets\n",
      _version_: 1759493524313604096,
    },
  ];

  const getResponseFromApi = (event) => {
    if (event.key === "Enter") {
      axios
        .get(api_url, {
          params: {
            query: text,
          },
        })
        .then((response) => setData(response.data));
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

    // Set the URLs as the sources for the iframes
    document.getElementById("google").src = googleUrl;
    document.getElementById("bing").src = bingUrl;
    // Call the API to get the search results
    axios
      .get(api_url, {
        params: {
          query: input,
        },
      })
      .then((response) => setData(response.data));
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
            name="type"
            value="page_rank"
          />
          <label id="page_rank_label" htmlFor="page_rank">
            Page Rank
          </label>
          <input
            type="radio"
            id="hits"
            name="type"
            value="hits"
            className="margin"
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
            name="type"
            value="flat_clustering"
          />
          <label id="flat_clustering_label" htmlFor="flat_clustering">
            Flat Clustering
          </label>
          <input
            type="radio"
            id="hierarchical_clustering"
            name="type"
            value="hierarchical_clustering"
            className="margin"
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
            name="type"
            value="association_qe"
          />
          <label id="association_qe_label" htmlFor="association_qe">
            Association
          </label>
          <input type="radio" id="metric_qe" name="type" value="metric_qe" />
          <label id="metric_qe_label" htmlFor="metric_qe">
            Metric
          </label>
          <input type="radio" id="scalar_qe" name="type" value="scalar_qe" />
          <label id="scalar_qe_label" htmlFor="query_expansion">
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
          onSubmit={(e) => getResponseFromApi(e)}
        />
        <hr />
      </form>

      {/* data && data.map((item) => <p>{item.title}</p>) */}
      <div className="container">
        {dummydata.map((item) => (
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
