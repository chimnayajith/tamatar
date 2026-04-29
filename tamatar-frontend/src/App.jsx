import { useState } from 'react';
import ImageUpload from './components/ImageUpload';
import ResultDisplay from './components/ResultDisplay';
import { predictDisease } from './services/api';
import { diseaseMap } from './data/diseaseData';
import './App.css';
import tomatoLogo from "./assets/tomato.png";

function App() {
  const [selectedImage, setSelectedImage] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleImageSelect = (file) => {
    setSelectedImage(file);
    setResult(null);
    setError(null);
  };

  const handleSubmit = async () => {
    if (!selectedImage) {
      setError('Please select an image first');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      // 🔥 FAKE API DELAY
      await new Promise(resolve => setTimeout(resolve, 2000));

      // 🔥 MOCK RESPONSE (like backend would return)
      const prediction = {
        class: "Tomato___Late_blight",
        confidence: 0.973
      };

      const mapped = diseaseMap[prediction.class] || {
        label: prediction.class,
        severity: "Healthy",
        description: "No disease detected.",
        actions: [
          "Continue regular care",
          "Monitor plant health"
        ]
      };

      setResult({
        label: mapped.label,
        severity: mapped.severity,
        description: mapped.description,
        actions: mapped.actions,
        confidence: (prediction.confidence * 100).toFixed(1)
      });

    } catch (err) {
      setError("Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setSelectedImage(null);
    setResult(null);
    setError(null);
  };

  return (
    <div className="app">

      {/* Header */}
      <header className="app-header">
        <img src={tomatoLogo} alt="tomato" className="logo-img" />

        <h1>Tomato Disease Detector</h1>
        <p>
          Upload a photo of your tomato plant leaf for instant disease detection
        </p>
      </header>

      <main className="app-main">
        <div className="main-card">

          {/* ALWAYS show image if selected */}
          <ImageUpload
            onImageSelect={handleImageSelect}
            image={selectedImage}
            onClear={handleReset}
          />

          {/* Show analyze button only before result */}
          {selectedImage && !result && (
            loading ? (
              <div className="loading-box">
                <span className="loader"></span>
                  <img src={tomatoLogo} alt="tomato" className="inline-icon" />
                  Analyzing tomato leaf...
              </div>
            ) : (
              <button className="submit-button" onClick={handleSubmit}>
                Analyze Image
              </button>
            )
          )}

          {/* Show result BELOW image */}
          {result && (
            <ResultDisplay
              result={result}
              onReset={handleReset}
            />
          )}

          {/* Error */}
          {error && error.trim() !== "" && (
            <div className="error-message">
              ⚠️ {error}
            </div>
          )}

        </div>
      </main>

    </div>
  );
}

export default App;