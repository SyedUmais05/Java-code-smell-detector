import React, { useState } from 'react';
import axios from 'axios';
import CodeInput from './components/CodeInput';
import Report from './components/Report';
import './index.css';

function App() {
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleAnalyze = async (code) => {
    setLoading(true);
    setReport(null);
    try {
      const response = await axios.post('http://localhost:8000/analyze', {
        sourceCode: code
      });
      setReport(response.data);
    } catch (error) {
      console.error("Analysis failed", error);
      setReport({
        error: error.response?.data?.detail || "Failed to connect to analysis server. Is backend running?"
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <header>
        <h1>Code Smell Detector</h1>
        <p>Static Analysis for Academic Re-Engineering</p>
      </header>

      <CodeInput onAnalyze={handleAnalyze} isLoading={loading} />
      <Report data={report} />
    </div>
  );
}

export default App;
