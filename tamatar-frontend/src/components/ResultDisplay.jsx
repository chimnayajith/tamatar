/**
 * ResultDisplay Component
 * Displays the prediction results with disease name and confidence
 */

import './ResultDisplay.css';

const ResultDisplay = ({ result }) => {
  if (!result) return null;

  const { disease, confidence } = result;
  
  // Determine confidence level for styling
  const confidenceLevel = confidence >= 0.8 ? 'high' : confidence >= 0.5 ? 'medium' : 'low';
  
  return (
    <div className="result-display">
      <h2>Analysis Result</h2>
      
      <div className="result-card">
        <div className="disease-info">
          <span className="label">Detected Disease:</span>
          <h3 className="disease-name">{disease}</h3>
        </div>
        
        <div className="confidence-info">
          <span className="label">Confidence:</span>
          <div className={`confidence-bar-container ${confidenceLevel}`}>
            <div 
              className="confidence-bar" 
              style={{ width: `${confidence * 100}%` }}
            />
          </div>
          <span className="confidence-value">
            {(confidence * 100).toFixed(1)}%
          </span>
        </div>
        
        {/* Confidence interpretation */}
        <div className="confidence-message">
          {confidence >= 0.8 && (
            <p className="high">✓ High confidence - Result is reliable</p>
          )}
          {confidence >= 0.5 && confidence < 0.8 && (
            <p className="medium">⚠ Medium confidence - Consider retaking image</p>
          )}
          {confidence < 0.5 && (
            <p className="low">⚠ Low confidence - Please retake with better lighting</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default ResultDisplay;
