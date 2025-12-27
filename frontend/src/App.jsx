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
    // Clear previous report to trigger animation on new one nicely
    setReport(null);

    // Simulate a tiny delay for better UX (so it doesn't flash too fast if local)
    // await new Promise(r => setTimeout(r, 600)); 

    try {
      const response = await axios.post('http://localhost:8000/analyze', {
        sourceCode: code
      });
      setReport(response.data);
    } catch (error) {
      console.error("Analysis failed", error);
      setReport({
        error: error.response?.data?.detail || "Could not connect to analysis engine."
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <header>
        <h1>Java Code Smell Detection Tool</h1>
        <p>Automated static analysis to identify code quality issues and maintainability risks.</p>
      </header>

      <div className="main-content">
        <CodeInput onAnalyze={handleAnalyze} isLoading={loading} />
        <Report data={report} isLoading={loading} />
      </div>
    </div>
  );
}

export default App;
