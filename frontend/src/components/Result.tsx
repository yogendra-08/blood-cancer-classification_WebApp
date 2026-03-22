import React, { useState } from 'react';
import { PredictionResult, API_BASE_URL } from '../services/api';

interface ResultProps {
  result: PredictionResult;
  onReset?: () => void;
}

interface UserData {
  name: string;
  age: string;
  gender: string;
  mobile: string;
}

const Result: React.FC<ResultProps> = ({ result, onReset }) => {
  const { prediction, gradcam_url } = result;
  const [showModal, setShowModal] = useState(false);
  const [formData, setFormData] = useState<UserData>({
    name: '',
    age: '',
    gender: '',
    mobile: ''
  });
  const [isDownloading, setIsDownloading] = useState(false);

  const getGradcamUrl = () => {
    if (gradcam_url) {
      // Use the same base URL as the API
      return `${API_BASE_URL}${gradcam_url}`;
    }
    return '';
  };

  const handleDownloadPdf = () => {
    setShowModal(true);
  };

  const handleFormSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    // Validate form
    if (!formData.name || !formData.age || !formData.gender || !formData.mobile) {
      alert('Please fill all fields');
      return;
    }

    setIsDownloading(true);

    try {
      const formDataToSend = new FormData();
      formDataToSend.append('name', formData.name);
      formDataToSend.append('age', formData.age);
      formDataToSend.append('gender', formData.gender);
      formDataToSend.append('mobile', formData.mobile);
      formDataToSend.append('predicted_class', prediction.class);
      formDataToSend.append('confidence', prediction.confidence.toString());
      formDataToSend.append('input_image_url', ''); // Will be determined by latest upload
      formDataToSend.append('gradcam_image_url', gradcam_url || '');

      const response = await fetch(`${API_BASE_URL}/save-result`, {
        method: 'POST',
        body: formDataToSend
      });

      const data = await response.json();
      console.log('Response from server:', data);

      if (data.success && data.pdf_content) {
        console.log('PDF content received, downloading...');
        // Download PDF
        const pdfBlob = new Blob([atob(data.pdf_content)], { type: 'application/pdf' });
        const pdfUrl = URL.createObjectURL(pdfBlob);
        const a = document.createElement('a');
        a.href = pdfUrl;
        a.download = `blood-cancer-report-${formData.name.replace(/\s+/g, '-').toLowerCase()}.pdf`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(pdfUrl);
        
        setShowModal(false);
        alert('Report downloaded successfully!');
      } else {
        console.log('PDF generation failed:', data);
        alert('Failed to generate report: ' + (data.message || 'Unknown error'));
      }
    } catch (error) {
      console.error('Error downloading PDF:', error);
      alert('Failed to download report. Please try again.');
    } finally {
      setIsDownloading(false);
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
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

      <div style={{ textAlign: 'center', marginTop: '20px' }}>
        <button
          onClick={handleDownloadPdf}
          className="download-pdf-btn"
          style={{
            backgroundColor: '#667eea',
            color: 'white',
            border: 'none',
            padding: '12px 24px',
            borderRadius: '8px',
            fontSize: '16px',
            cursor: 'pointer',
            transition: 'background-color 0.3s'
          }}
          onMouseOver={(e) => e.currentTarget.style.backgroundColor = '#5a67d8'}
          onMouseOut={(e) => e.currentTarget.style.backgroundColor = '#667eea'}
        >
          📄 Download PDF Report
        </button>
      </div>

      {showModal && (
        <div className="modal-overlay" style={{
          position: 'fixed',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          backgroundColor: 'rgba(0, 0, 0, 0.5)',
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          zIndex: 1000
        }}>
          <div className="modal-content" style={{
            backgroundColor: 'white',
            padding: '30px',
            borderRadius: '12px',
            maxWidth: '400px',
            width: '90%',
            boxShadow: '0 10px 25px rgba(0, 0, 0, 0.2)'
          }}>
            <h3 style={{ marginBottom: '20px', color: '#333' }}>Patient Details</h3>
            <form onSubmit={handleFormSubmit}>
              <div style={{ marginBottom: '15px' }}>
                <label style={{ display: 'block', marginBottom: '5px', color: '#555' }}>Name *</label>
                <input
                  type="text"
                  name="name"
                  value={formData.name}
                  onChange={handleInputChange}
                  required
                  style={{
                    width: '100%',
                    padding: '8px',
                    border: '1px solid #ddd',
                    borderRadius: '4px',
                    fontSize: '14px'
                  }}
                />
              </div>
              
              <div style={{ marginBottom: '15px' }}>
                <label style={{ display: 'block', marginBottom: '5px', color: '#555' }}>Age *</label>
                <input
                  type="number"
                  name="age"
                  value={formData.age}
                  onChange={handleInputChange}
                  required
                  min="1"
                  max="120"
                  style={{
                    width: '100%',
                    padding: '8px',
                    border: '1px solid #ddd',
                    borderRadius: '4px',
                    fontSize: '14px'
                  }}
                />
              </div>
              
              <div style={{ marginBottom: '15px' }}>
                <label style={{ display: 'block', marginBottom: '5px', color: '#555' }}>Gender *</label>
                <select
                  name="gender"
                  value={formData.gender}
                  onChange={handleInputChange}
                  required
                  style={{
                    width: '100%',
                    padding: '8px',
                    border: '1px solid #ddd',
                    borderRadius: '4px',
                    fontSize: '14px'
                  }}
                >
                  <option value="">Select Gender</option>
                  <option value="Male">Male</option>
                  <option value="Female">Female</option>
                  <option value="Other">Other</option>
                </select>
              </div>
              
              <div style={{ marginBottom: '20px' }}>
                <label style={{ display: 'block', marginBottom: '5px', color: '#555' }}>Mobile Number *</label>
                <input
                  type="tel"
                  name="mobile"
                  value={formData.mobile}
                  onChange={handleInputChange}
                  required
                  pattern="[0-9]{10}"
                  placeholder="1234567890"
                  style={{
                    width: '100%',
                    padding: '8px',
                    border: '1px solid #ddd',
                    borderRadius: '4px',
                    fontSize: '14px'
                  }}
                />
              </div>
              
              <div style={{ display: 'flex', gap: '10px', justifyContent: 'flex-end' }}>
                <button
                  type="button"
                  onClick={() => setShowModal(false)}
                  disabled={isDownloading}
                  style={{
                    padding: '8px 16px',
                    border: '1px solid #ddd',
                    backgroundColor: 'white',
                    borderRadius: '4px',
                    cursor: isDownloading ? 'not-allowed' : 'pointer'
                  }}
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={isDownloading}
                  style={{
                    padding: '8px 16px',
                    border: 'none',
                    backgroundColor: '#667eea',
                    color: 'white',
                    borderRadius: '4px',
                    cursor: isDownloading ? 'not-allowed' : 'pointer'
                  }}
                >
                  {isDownloading ? 'Generating...' : 'Download PDF'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default Result;
