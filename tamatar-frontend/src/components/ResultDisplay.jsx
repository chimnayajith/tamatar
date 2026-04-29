import './ResultDisplay.css';

const ResultDisplay = ({ result, onReset }) => {
  if (!result) return null;

  console.log(result);

  const { label, confidence, description, actions, severity } = result;

  const isHealthy = severity === "Healthy";
  const color =
    severity === "Healthy"
      ? "green"
      : severity === "Moderate"
      ? "orange"
      : "red";

  return (
    <div className="result-card">

      {/* ICON + CONTENT */}
      <div className="header-row">

        <div className={`icon-box ${color}`}>
          {isHealthy ? "✓" : "⚠"}
        </div>

        <div className="header-text">

          {/* TITLE */}
          <h2 className="disease-title">{label}</h2>

          {/* BADGE */}
          <span className={`badge ${color}`}>
            {severity}
          </span>

          {/* CONFIDENCE */}
          <p className="confidence-text">
            Confidence: <b>{confidence}%</b>
          </p>

          <div className="progress-bar">
            <div
              className={`progress ${color}`}
              style={{ width: `${confidence}%` }}
            />
          </div>

          {/* DESCRIPTION */}
          <p className="description">
            {isHealthy
              ? "No disease detected. Plant appears healthy."
              : description}
          </p>

        </div>
      </div>

      <div className="divider"></div>

      {/* ACTIONS */}
      <div className="actions">
        <h3>{isHealthy ? "Care Tips" : "Recommended Actions"}</h3>

        <ul>
          {actions.map((a, i) => (
            <li key={i}>
              <span className="step">{i + 1}</span>
              <span>{a}</span>
            </li>
          ))}
        </ul>
      </div>

      {/* NOTE */}
      {!isHealthy && (
        <div className="note">
          <b>Note:</b> This is an automated analysis. For severe cases consult a plant expert.
        </div>
      )}

      {/* BUTTON */}
      <button className="reset-btn" onClick={onReset}>
        Analyze Another Tomato Leaf
      </button>

    </div>
  );
};

export default ResultDisplay;