import React, { useState } from 'react';

const CodeInput = ({ onAnalyze, isLoading }) => {
  const [code, setCode] = useState(`public class SmellyClass {
    // 1. Primitive Obsession
    private int id;
    private String name;
    private String email;
    // ...

    // 3. Long Method
    public void complexLogic(int type) {
        System.out.println("Start");
        int result = 0;
        switch (type) { 
            case 1: result = 10; break;
            case 2: result = 20; break;
            case 3: result = 30; break;
            case 4: result = 40; break;
            case 5: result = 50; break;
            case 6: result = 60; break; 
        }
        // ... more logic ...
    }
}`);

  const lineCount = code.split('\n').length;
  const isOverLimit = lineCount > 500;

  // Generate line numbers
  const lineNumbers = Array.from({ length: lineCount }, (_, i) => i + 1).join('\n');

  const handleScroll = (e) => {
    const gutter = document.getElementById('line-gutter');
    if (gutter) {
      gutter.scrollTop = e.target.scrollTop;
    }
  };

  return (
    <div className="panel input-panel">
      <div className="panel-header">
        <h2>
          <span>💻</span> Source Code
        </h2>
      </div>

      <div className="panel-body">
        <div className="editor-wrapper">
          <div className="editor-container">
            <div className="line-gutter" id="line-gutter">
              <pre>{lineNumbers}</pre>
            </div>
            <textarea
              className="code-editor"
              value={code}
              onChange={(e) => setCode(e.target.value)}
              onScroll={handleScroll}
              placeholder="// Paste your Java Class here..."
              disabled={isLoading}
              spellCheck="false"
            />
          </div>
        </div>
      </div>

      <div className="action-bar">
        <div className="line-count" style={{ color: isOverLimit ? '#ef4444' : 'inherit' }}>
          {lineCount} lines {isOverLimit && '(Limit: 500)'}
        </div>
        <button
          className="btn-primary"
          onClick={() => onAnalyze(code)}
          disabled={isLoading || !code.trim() || isOverLimit}
        >
          {isLoading ? 'Scanning...' : 'Analyze Code'}
        </button>
      </div>
    </div>
  );
};

export default CodeInput;
