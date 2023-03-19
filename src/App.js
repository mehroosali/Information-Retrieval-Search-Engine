import './App.css';
import React, { useState } from 'react';
import axios from 'axios';

const api_url = 'http://localhost:5000/api'

function App() {
  document.title = 'Search Engine'
  const [text, setText] = useState('');
  const [data, setData] = useState([]);

  const getResponseFromApi = (event) => {
    if (event.key === "Enter") {
      axios.get(api_url, {
        params: {
          query:text
        }
      }).then(response => setData(response.data))
    }
    
  }
  return (
    <div className='App'>
      <h1>Sweets Search Engine</h1>
      <input value={text}
        type = 'text'
        placeholder='Enter sweet name'
        onChange={e => setText(e.target.value)}
        onKeyDown={e => getResponseFromApi(e)}
      />
      {data && data.map(item => (
          <p>{item.title}</p>
      ))}
    </div>
  );
}

export default App;
