import React from 'react';

const Report = ({ data, isLoading }) => {

  if (isLoading) {
    return (
      <div className="panel report-panel">
        <div className="panel-header">
          <h2><span>📊</span> Analysis Report</h2>
        </div>
        <div className="empty-state">
          <div className="empty-icon">⏳</div>
          <p>Analyzing code structure...</p>
        </div>
      </div>
    )
  }

  if (!data) {
    return (
      <div className="panel report-panel">
        <div className="panel-header">
          <h2><span>📊</span> Analysis Report</h2>
        </div>
        <div className="empty-state">
          <div className="empty-icon">👋</div>
          <p>Ready to analyze. Run a scan to see results here.</p>
        </div>
      </div>
    )
  }

  if (data.error) {
    return (
      <div className="panel report-panel">
        <div className="panel-header">
          <h2><span>⚠️</span> Error</h2>
        </div>
        <div className="empty-state" style={{ color: '#ef4444' }}>
          <p>{data.error}</p>
        </div>
      </div>
    );
  }

  const { summary, smells } = data;

  return (
    <div className="panel report-panel fade-in">
      <div className="panel-header">
        <h2><span>📊</span> Analysis Report</h2>
      </div>

      <div className="stats-grid">
        <div className="stat-card">
          <span className="stat-value">{summary.totalLines}</span>
          <span className="stat-label">Lines of Code</span>
        </div>
        <div className="stat-card" style={{ borderColor: summary.totalSmells > 0 ? 'var(--severity-medium)' : 'var(--severity-low)' }}>
          <span className="stat-value" style={{ color: summary.totalSmells > 0 ? 'var(--severity-high)' : 'var(--severity-low)' }}>
            {summary.totalSmells}
          </span>
          <span className="stat-label">Identified Smells</span>
        </div>
      </div>

      <div className="smell-feed">
        {smells.length === 0 ? (
          <div className="empty-state">
            <div className="empty-icon">✅</div>
            <p>No code smells detected. Great job!</p>
          </div>
        ) : (
          smells.map((smell, index) => (
            <div key={index} className={`smell-card card-severity-${smell.severity}`}>
              <div className="card-header">
                <span className="smell-title">{smell.type}</span>
                <span className={`badge badge-${smell.severity}`}>{smell.severity} Priority</span>
              </div>

              <div className="card-row">
                <span className="card-label">Location:</span>
                <span className="card-value">{smell.location}</span>
              </div>
              <div className="card-row">
                <span className="card-label">Issue:</span>
                <span className="card-value">{smell.reason}</span>
              </div>

              <div className="refactor-tip">
                <span>💡 Suggested Fix: </span>
                <span>{smell.suggestedRefactoring}</span>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default Report;
