import "./App.css";
import React, { useState } from "react";
import axios from "axios";
import "./styles.css";
import ClipLoader from "react-spinners/ClipLoader";
import { Tab, Tabs, TabList, TabPanel } from "react-tabs";
import "react-tabs/style/react-tabs.css";

const api_url = "http://localhost:5000/api";

function App() {
  document.title = "Search Engine";
  const [text, setText] = useState("");
  const [data, setData] = useState([]);
  const [relevanceOption, setRelevanceOption] = useState("");
  const [clusteringOption, setClusteringOption] = useState("");
  const [queryExpOption, setQueryExpOption] = useState("");
  const [qeResult, setQeResult] = useState("");
  const [loading, setLoading] = useState(false);
  const [googleUrl, setGoogleUrl] = useState("");
  const [bingUrl, setBingUrl] = useState("");
  const [qeVisible, setQeVisible] = useState(false); 

  const getResponseFromApi = (event) => {
    if (event.key === "Enter") {
      axios
        .get(api_url, {
          params: {
            query: text,
          },
        })
        .then((response) => {
          setData(response.data.query_results.slice(0, 25));
        });
    }
  };

  const handleSearch = (event) => {
    event.preventDefault();
    setData([]);
    setQeResult("");
    setLoading(true);
    setQeVisible(false);
    const qexpElement = document.getElementById("qexp");
    if (qexpElement) {
      qexpElement.style.display = "none";
    }
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
    } else if (clusteringOption === "single-HAC_clustering") {
      params.co = "single";
    }else if(clusteringOption==="average-HAC_clustering"){
      params.co="average"
    }

    if (queryExpOption === "association_qe") {
      params.qe = "association";
    } else if (queryExpOption === "scalar_qe") {
      params.qe = "scalar";
    } else if (queryExpOption === "metric_qe") {
      params.qe = "metric";
    }
    // try {
    //   if ("qe" in params) {
    //     setQeVisible(true);
    //     // document.getElementById("qexp").style.display = "block";
    //   } else {
    //     // document.getElementById("qexp").style.display = "none";
    //     setQeVisible(false);
    //   }
    // } catch (error) {
    //   console.log(error);
    // }

    axios.get(api_url, { params }).then((response) => {
      setData(response.data.query_results.slice(0, 25));
      setLoading(false);
      if ("qe" in params) {
        setQeVisible(true);
        handleQEResults(response.data.query);
      } else {
        setGoogleUrl(
          "https://www.google.com/search?igu=1&source=hp&ei=lheWXriYJ4PktQXN-LPgDA&q=" +
            response.data.query
        );
        setBingUrl("https://www.bing.com/search?q=" + response.data.query);
        displayBingAndGoogle(response.data.query);
      }
    });
  };

  // const displayBingAndGoogle = (query) => {
  //           // Build the URLs for Google and Bing search
  //   const googleUrl =
  //     "https://www.google.com/search?igu=1&source=hp&ei=lheWXriYJ4PktQXN-LPgDA&q=" +
  //     query;
  //   const bingUrl = "https://www.bing.com/search?q=" + query;

  //   // Set the URLs as the sources for the iframes
  //   document.getElementById("google").src = googleUrl;
  //   document.getElementById("bing").src = bingUrl;
  // }
  const displayBingAndGoogle = (query) => {
    // Build the URLs for Google and Bing search
    // const googleUrl =
    //   "https://www.google.com/search?igu=1&source=hp&ei=lheWXriYJ4PktQXN-LPgDA&q=" +
    //   query;
    // const bingUrl = "https://www.bing.com/search?q=" + query;

    // Set the URLs as the sources for the iframes
    const activeTab = document.querySelector(".react-tabs__tab--selected");
    if (activeTab.innerHTML === "Google") {
      document.getElementById("google").src = googleUrl;
      console.log("function in google tab is called");
    } else if (activeTab.innerHTML === "Bing") {
      document.getElementById("bing").src = bingUrl;
    }
  };

  const handleQEResults = (expanded_query) => {
    expanded_query = expanded_query.replace(/"/g, "");
    setQeResult(expanded_query);
    setGoogleUrl(
      "https://www.google.com/search?igu=1&source=hp&ei=lheWXriYJ4PktQXN-LPgDA&q=" +
        expanded_query
    );
    setBingUrl("https://www.bing.com/search?q=" + expanded_query);
    displayBingAndGoogle(expanded_query);
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
            onClick={(e) => {
              if (relevanceOption === e.target.value) {
                setRelevanceOption("");
                e.target.checked = false;
                console.log("2");

                console.log(relevanceOption);
              } else {
                setRelevanceOption(e.target.value);
                console.log("1");

                console.log(relevanceOption);
              }
            }}
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
            onClick={(e) => {
              if (relevanceOption === e.target.value) {
                setRelevanceOption("");
                e.target.checked = false;
              } else {
                setRelevanceOption(e.target.value);
              }
            }}
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
            onClick={(e) => {
              if (clusteringOption === e.target.value) {
                setClusteringOption("");
                e.target.checked = false;
              } else {
                setClusteringOption(e.target.value);
              }
            }}
          />
          <label id="flat_clustering_label" htmlFor="flat_clustering">
            Flat
          </label>
          <input
            type="radio"
            id="single-HAC_clustering"
            name="co"
            value="single-HAC_clustering"
            className="margin"
            checked={clusteringOption === "single-HAC_clustering"}
            onClick={(e) => {
              if (clusteringOption === e.target.value) {
                setClusteringOption("");
                e.target.checked = false;
              } else {
                setClusteringOption(e.target.value);
              }
            }}
          />
          <label
            id="single-HAC_clustering_label"
            htmlFor="single-HAC_clustering"
          >
            Single-HAC
          </label>
          <input
            type="radio"
            id="average-HAC_clustering"
            name="co"
            value="average-HAC_clustering"
            checked={clusteringOption === "average-HAC_clustering"}
            onClick={(e) => {
              if (clusteringOption === e.target.value) {
                setClusteringOption("");
                e.target.checked = false;
              } else {
                setClusteringOption(e.target.value);
              }
            }}
          />
          <label id="average-HAC_clustering_label" htmlFor="average-HAC_clustering">
          Average-HAC
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
            onClick={(e) => {
              if (queryExpOption === e.target.value) {
                setQueryExpOption("");
                e.target.checked = false;
              } else {
                setQueryExpOption(e.target.value);
              }
            }}
          />
          <label id="association_qe_label" htmlFor="association_qe">
            Association
          </label>
          <input
            type="radio"
            id="metric_qe"
            name="qe"
            value="metric_qe"
            checked={queryExpOption === "metric_qe"}
            onClick={(e) => {
              if (queryExpOption === e.target.value) {
                setQueryExpOption("");
                e.target.checked = false;
              } else {
                setQueryExpOption(e.target.value);
              }
            }}
          />
          <label id="metric_qe_label" htmlFor="metric_qe">
            Metric
          </label>
          <input
            type="radio"
            id="scalar_qe"
            name="qe"
            value="scalar_qe"
            checked={queryExpOption === "scalar_qe"}
            onClick={(e) => {
              if (queryExpOption === e.target.value) {
                setQueryExpOption("");
                e.target.checked = false;
              } else {
                setQueryExpOption(e.target.value);
              }
            }}
          />
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
      <br />
      <Tabs>
        <TabList>
          <Tab>Results</Tab>
          <Tab>Google</Tab>
          <Tab>Bing</Tab>
        </TabList>

        <TabPanel>
          {/* Default Results */}
          {/* Add your existing code to display the search results here */}
          {qeVisible && (<div className="qeParagraph" id="qexp" >
            <p className="qeSub">Expanded query: {qeResult ? qeResult : ""}</p>
          </div>)}
          

          <div className="container">
            <div className="spinner">
              <ClipLoader
                color="#ffffff"
                loading={loading}
                size={50}
                aria-label="Loading Spinner"
                data-testid="loader"
              />
            </div>
            {data.map((item) => (
              <div className="card" key={item.id}>
                <h2 className="card-title">{item.title}</h2>

                <a
                  className="card-link"
                  href={item.url}
                  target="_blank"
                  rel="noreferrer"
                >
                  {item.url}
                </a>
                <p className="card-content">{item.content.slice(0, 200)}</p>
              </div>
            ))}
          </div>
        </TabPanel>
        <TabPanel>
          {/* Google Results */}
          <iframe id="google" title="Google" src={googleUrl}></iframe>{" "}
        </TabPanel>
        <TabPanel>
          {/* Bing Results */}

          <iframe id="bing" title="Bing" src={bingUrl}></iframe>
        </TabPanel>
      </Tabs>

      {/* data && data.map((item) => <p>{item.title}</p>) } */}
    </div>
  );
}

export default App;
