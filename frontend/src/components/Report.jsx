import React from 'react';

const Report = ({ data }) => {
  if (!data) return null;

  if (data.error) {
    return <div className="error-banner">{data.error}</div>;
  }

  const { summary, smells } = data;

  return (
    <div className="report-container">
      <h2>Analysis Report</h2>

      <div className="summary-cards">
        <div className="card">
          <h3>Total Lines</h3>
          <p>{summary.totalLines}</p>
        </div>
        <div className="card">
          <h3>Detected Smells</h3>
          <p className={summary.totalSmells > 0 ? "highlight-bad" : "highlight-good"}>
            {summary.totalSmells}
          </p>
        </div>
      </div>

      <h3>Detailed Smell List</h3>
      {smells.length === 0 ? (
        <p className="clean-message">✅ No classic code smells detected.</p>
      ) : (
        <div className="smell-list">
          {smells.map((smell, index) => (
            <div key={index} className={`smell-item severity-${smell.severity.toLowerCase()}`}>
              <div className="smell-header">
                <span className="smell-type">{smell.type}</span>
                <span className={`severity-tag ${smell.severity.toLowerCase()}`}>{smell.severity}</span>
              </div>
              <div className="smell-details">
                <p><strong>Location:</strong> {smell.location}</p>
                <p><strong>Reason:</strong> {smell.reason}</p>
                <p><strong>Refactoring:</strong> <em>{smell.suggestedRefactoring}</em></p>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default Report;
