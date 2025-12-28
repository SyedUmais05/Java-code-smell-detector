import React, { useState } from 'react';
import CodeInput from '../components/CodeInput';
import Report from '../components/Report';
import axios from 'axios';

const Analyzer = () => {
    const [report, setReport] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const handleAnalyze = async (code) => {
        setLoading(true);
        setReport(null);
        setError('');

        try {
            const response = await axios.post('http://localhost:8000/analyze', {
                sourceCode: code
            });
            setReport(response.data);
        } catch (err) {
            console.error(err);
            let msg = err.response?.data?.detail || err.message || "Connection refused";
            if (typeof msg === 'object') msg = JSON.stringify(msg);
            setError(`Connection Error: ${msg}. Check if backend is running on port 8000.`);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="app-container">
            <header className="analyzer-header">
                <h1>Code Analyzer</h1>
                <p>Paste your Java code below to detect smells</p>
            </header>

            <div className="main-content">
                <CodeInput onAnalyze={handleAnalyze} isLoading={loading} />

                {error && (
                    <div className="panel error-panel">
                        <div className="panel-body" style={{ padding: '2rem', color: '#ef4444', textAlign: 'center' }}>
                            <strong>Error:</strong> {error}
                        </div>
                    </div>
                )}

                <Report data={report} />
            </div>
        </div>
    );
};

export default Analyzer;
