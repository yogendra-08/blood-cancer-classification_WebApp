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
    </div>
  );
};

const App: React.FC = () => {
  return <AppContent />;
};

export default App;
