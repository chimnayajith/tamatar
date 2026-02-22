/**
 * Main App Component
 * Integrates all components and handles the prediction workflow
 */

import { useState } from 'react';
import ImageUpload from './components/ImageUpload';
import ResultDisplay from './components/ResultDisplay';
import { predictDisease } from './services/api';
import './App.css';

function App() {
  const [selectedImage, setSelectedImage] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  /**
   * Handle image selection from ImageUpload component
   */
  const handleImageSelect = (file) => {
    setSelectedImage(file);
    setResult(null);
    setError(null);
  };

  /**
   * Submit image for disease prediction
   */
  const handleSubmit = async () => {
    if (!selectedImage) {
      setError('Please select an image first');
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      // Call API to predict disease
      const prediction = await predictDisease(selectedImage);
      setResult(prediction);
    } catch (err) {
      setError(err.message || 'Failed to analyze image. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  /**
   * Reset the app to initial state
   */
  const handleReset = () => {
    setSelectedImage(null);
    setResult(null);
    setError(null);
  };

  return (
    <div className="app">
      {/* Header */}
      <header className="app-header">
        <h1>🍅 Tamatar</h1>
        <p>Tomato Leaf Disease Detection</p>
      </header>

      {/* Main Content */}
      <main className="app-main">
        {/* Image Upload Component */}
        <ImageUpload 
          onImageSelect={handleImageSelect} 
          disabled={loading}
        />

        {/* Submit Button */}
        {selectedImage && !result && (
          <button 
            className="submit-button"
            onClick={handleSubmit}
            disabled={loading}
          >
            {loading ? (
              <>
                <span className="spinner"></span>
                Analyzing...
              </>
            ) : (
              'Analyze Image'
            )}
          </button>
        )}

        {/* Error Message */}
        {error && (
          <div className="error-message">
            <span className="error-icon">⚠️</span>
            <p>{error}</p>
            <button onClick={() => setError(null)}>Dismiss</button>
          </div>
        )}

        {/* Result Display */}
        <ResultDisplay result={result} />

        {/* Reset Button */}
        {result && (
          <button 
            className="reset-button"
            onClick={handleReset}
          >
            Analyze Another Image
          </button>
        )}
      </main>

      {/* Footer */}
      <footer className="app-footer">
        <p>Powered by AI • PWA Ready</p>
      </footer>
    </div>
  );
}

export default App;
