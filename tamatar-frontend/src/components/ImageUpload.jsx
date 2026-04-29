import { useState, useRef, useEffect } from "react";
import "./ImageUpload.css";
import imageIcon from "../assets/images.svg";
import fileIcon from "../assets/file.svg";
import cameraIcon from "../assets/camera.svg";
import closeIcon from "../assets/close.svg";

const ImageUpload = ({ onImageSelect, image, onClear }) => {
  const fileRef = useRef(null);
  const cameraRef = useRef(null);
  const [previewUrl, setPreviewUrl] = useState(null);

  useEffect(() => {
    if (image) {
      const url = URL.createObjectURL(image);
      setPreviewUrl(url);
      return () => URL.revokeObjectURL(url);
    } else {
      setPreviewUrl(null);
    }
  }, [image]);

  const handleFile = (e) => {
    const file = e.target.files && e.target.files[0];
    if (file) {
      onImageSelect(file);
    }
    e.target.value = "";
  };

  return (
    <div className="upload-card">

      <input
        type="file"
        ref={fileRef}
        hidden
        accept="image/*"
        onChange={handleFile}
      />

      <input
        type="file"
        ref={cameraRef}
        hidden
        accept="image/*"
        capture="environment"
        onChange={handleFile}
      />

      {/* IF IMAGE EXISTS → SHOW PREVIEW */}
      {image ? (
        <div className="preview-card">
          
          <div className="preview-header">
            <span>Uploaded Image</span>
            <button className="close-btn" onClick={onClear}>
              <img src={closeIcon} alt="close" />
            </button>
          </div>

          <div className="preview-image-wrapper">
            <img
              src={previewUrl}
              alt="preview"
              className="preview-image"
            />
          </div>

          <div className="preview-actions">
            <button
              className="btn primary"
              onClick={() => {
                if (fileRef.current) {
                  fileRef.current.value = "";
                  fileRef.current.click();
                }
              }}
            >
              <img src={fileIcon} alt="file" className="btn-icon" />
              Re-upload
            </button>

            <button
              className="btn secondary"
              onClick={() => {
                if (cameraRef.current) {
                  cameraRef.current.value = "";
                  cameraRef.current.click();
                }
              }}
            >
              <img src={cameraIcon} alt="camera" className="btn-icon" />
              Retake Photo
            </button>
          </div>

        </div>
      ) : (
        <div className="upload-box">
          <div className="upload-icon">
            <img src={imageIcon} alt="upload" />
          </div>
            <p className="upload-title">Upload Tomato Leaf Photo</p>
            <p className="upload-subtext">
              Drag and drop an image here, or select from device
            </p>

          <button className="btn primary" onClick={() => { 
              if (fileRef.current) { 
                fileRef.current.value = ""; 
                fileRef.current.click(); 
              } 
            }}>
            <img src={fileIcon} alt="file" className="btn-icon" />
            Choose File
          </button>

          <button className="btn secondary" onClick={() => { 
              if (cameraRef.current) { 
                cameraRef.current.value = ""; 
                cameraRef.current.click(); 
              } 
            }}>
            <img src={cameraIcon} alt="camera" className="btn-icon" />
            Take Photo
          </button>
        </div>
      )}

    </div>
  );
};

export default ImageUpload;