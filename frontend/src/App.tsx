import React, { useState } from 'react';
import './index.css';
import Upload from './components/Upload';
import Result from './components/Result';

interface PredictionResult {
  success: boolean;
  prediction: {
    class: string;
    confidence: number;
    all_probabilities: Record<string, number>;
  };
  gradcam_url: string;
  timestamp: string;
}

const AppContent: React.FC = () => {
  const [predictionResult, setPredictionResult] = useState<PredictionResult | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handlePrediction = (result: PredictionResult) => {
    setPredictionResult(result);
    setIsLoading(false);
    setError(null);
  };

  const handleLoading = (loading: boolean) => {
    setIsLoading(loading);
  };

  const handleError = (errorMessage: string) => {
    setError(errorMessage);
    setIsLoading(false);
  };

  const handleReset = () => {
    setPredictionResult(null);
    setError(null);
  };

  // Register service worker for PWA
  React.useEffect(() => {
    if ('serviceWorker' in navigator) {
      navigator.serviceWorker.register('/sw.js')
        .then((registration) => {
          console.log('Service Worker registered with scope:', registration.scope);
        })
        .catch((error) => {
          console.log('Service Worker registration failed:', error);
        });
    }
  }, []);

  return (
    <div className="container">
      <div className="header">
        <h1>Blood Cancer Classifier</h1>
        <p>AI-powered blood cancer classification with explainable AI</p>
      </div>

      <div className="main-content">
        {error && (
          <div className="error-message">
            <p>❌ {error}</p>
          </div>
        )}

        <Upload
          onPrediction={handlePrediction}
          onLoading={handleLoading}
          onError={handleError}
          onReset={handleReset}
          loading={isLoading}
          hasResult={!!predictionResult}
        />

        {predictionResult && (
          <Result result={predictionResult} onReset={handleReset} />
        )}

        {isLoading && (
          <div className="loading">
            <div className="spinner"></div>
            <p>Analyzing image...</p>
          </div>
        )}
      </div>

      <footer className="app-footer" style={{
        textAlign: 'center',
        padding: '20px',
        marginTop: '40px',
        borderTop: '1px solid #eee',
        color: '#666'
      }}>
        <a 
          href="https://github.com/yogendra-08/blood-cancer-classification_WebApp"
          target="_blank"
          rel="noopener noreferrer"
          style={{
            color: '#667eea',
            textDecoration: 'none',
            display: 'inline-flex',
            alignItems: 'center',
            gap: '8px',
            fontSize: '14px'
          }}
        >
          <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
            <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
          </svg>
          Blood Cancer Classification Web App
        </a>
      </footer>
    </div>
  );
};

const App: React.FC = () => {
  return <AppContent />;
};

export default App;
