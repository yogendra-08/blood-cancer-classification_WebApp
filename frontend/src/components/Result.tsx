import React from 'react';
import { PredictionResult, API_BASE_URL } from '../services/api';

interface ResultProps {
  result: PredictionResult;
  onReset?: () => void;
}

const Result: React.FC<ResultProps> = ({ result, onReset }) => {
  const { prediction, gradcam_url } = result;

  const getGradcamUrl = () => {
    if (gradcam_url) {
      // Use the same base URL as the API
      return `${API_BASE_URL}${gradcam_url}`;
    }
    return '';
  };

  return (
    <div className="results-section active">
      <div className="result-header">
        <h2 className="result-title">Classification Result</h2>
        <div className="result-class">{prediction.class}</div>
        <div className="result-confidence">
          Confidence: {prediction.confidence.toFixed(2)}%
        </div>
      </div>

      <div className="confidence-bar">
        <div
          className="confidence-fill"
          style={{ width: `${prediction.confidence}%` }}
        >
          {prediction.confidence.toFixed(1)}%
        </div>
      </div>

      <h3>All Class Probabilities</h3>
      <div className="probabilities-grid">
        {Object.entries(prediction.all_probabilities).map(([className, probability]) => (
          <div
            key={className}
            className="probability-item"
            style={{
              borderLeftColor: className === prediction.class ? '#667eea' : '#ddd'
            }}
          >
            <div className="probability-label">{className}</div>
            <div className="probability-value">{probability.toFixed(2)}%</div>
          </div>
        ))}
      </div>

      {gradcam_url && (
        <div className="gradcam-section">
          <h3 className="gradcam-title">
            GradCAM Visualization
            <span className="tooltip">
              ℹ️
              <span className="tooltiptext">
                Red regions indicate areas where the model focused to make the prediction
              </span>
            </span>
          </h3>
          <div style={{ marginBottom: '10px', fontSize: '12px', color: '#666' }}>
            Debug: URL = {getGradcamUrl()}
          </div>
          <img
            src={getGradcamUrl()}
            alt="GradCAM visualization"
            className="gradcam-image"
            onLoad={() => console.log('GradCAM image loaded successfully')}
            onError={(e) => {
              console.error('Failed to load GradCAM image from:', getGradcamUrl());
              console.error('Error details:', e);
              e.currentTarget.style.display = 'none';
            }}
          />
        </div>
      )}

      <div style={{ textAlign: 'center', marginTop: '30px', color: 'var(--text-secondary)' }}>
        <small>Analysis completed at: {new Date(result.timestamp).toLocaleString()}</small>
      </div>
    </div>
  );
};

export default Result;
