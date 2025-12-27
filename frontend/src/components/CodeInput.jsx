import React, { useState } from 'react';

const CodeInput = ({ onAnalyze, isLoading }) => {
  const [code, setCode] = useState(`public class UserManager {
    private String name;
    private int age;
    private String address;
    // ... many fields ...

    public void processUser() {
        // ... long method ...
        System.out.println("Processing " + name);
        if (age > 18) {
             System.out.println("Adult");
             // ... more logic ...
        }
    }
}`);

  const handleSubmit = () => {
    onAnalyze(code);
  };

  return (
    <div className="input-container">
      <h2>Source Code Input</h2>
      <textarea
        value={code}
        onChange={(e) => setCode(e.target.value)}
        rows={20}
        placeholder="Paste Java code here..."
        disabled={isLoading}
      />
      <div className="actions">
        <button onClick={handleSubmit} disabled={isLoading}>
          {isLoading ? 'Analyzing...' : 'Analyze Code'}
        </button>
        <span className="hint">{code.split('\n').length} lines (Max 500)</span>
      </div>
    </div>
  );
};

export default CodeInput;
