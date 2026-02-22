/**
 * ImageUpload Component
 * Handles image selection from file picker or camera
 * Displays image preview
 */

import { useState, useRef } from 'react';
import './ImageUpload.css';

const ImageUpload = ({ onImageSelect, disabled }) => {
  const [preview, setPreview] = useState(null);
  const fileInputRef = useRef(null);

  /**
   * Handle file selection from input
   */
  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file && file.type.startsWith('image/')) {
      // Create preview URL
      const reader = new FileReader();
      reader.onloadend = () => {
        setPreview(reader.result);
      };
      reader.readAsDataURL(file);
      
      // Pass file to parent component
      onImageSelect(file);
    }
  };

  /**
   * Trigger file input click
   */
  const handleUploadClick = () => {
    fileInputRef.current?.click();
  };

  /**
   * Clear selected image
   */
  const handleClear = () => {
    setPreview(null);
    onImageSelect(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  return (
    <div className="image-upload">
      {/* Hidden file input with camera support */}
      <input
        ref={fileInputRef}
        type="file"
        accept="image/*"
        capture="environment" // Enable camera on mobile devices
        onChange={handleFileChange}
        disabled={disabled}
        style={{ display: 'none' }}
      />

      {/* Image preview or upload button */}
      {preview ? (
        <div className="preview-container">
          <img src={preview} alt="Preview" className="image-preview" />
          <button 
            onClick={handleClear} 
            className="clear-button"
            disabled={disabled}
          >
            ✕ Clear
          </button>
        </div>
      ) : (
        <div className="upload-prompt" onClick={handleUploadClick}>
          <div className="upload-icon">📷</div>
          <p>Click to upload or take a photo</p>
          <small>Support for JPG, PNG images</small>
        </div>
      )}

      {/* Alternative upload button when image is shown */}
      {preview && (
        <button 
          onClick={handleUploadClick} 
          className="change-button"
          disabled={disabled}
        >
          Change Image
        </button>
      )}
    </div>
  );
};

export default ImageUpload;
