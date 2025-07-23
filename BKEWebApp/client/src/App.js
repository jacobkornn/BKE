import React, { useState } from 'react';
import InputPanel from './components/InputPanel';
import OutputPanel from './components/OutputPanel';
import './App.css';

function App() {
  const [results, setResults] = useState([]);

  return (
    <div className="app-container">
      <div className="panel input-panel">
        <InputPanel setResults={setResults} />
      </div>
      <div className="panel output-panel">
        <OutputPanel results={results} />
      </div>
    </div>
  );
}

export default App;