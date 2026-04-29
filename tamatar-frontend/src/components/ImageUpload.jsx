import { useState, useRef } from "react";
import "./ImageUpload.css";
import imageIcon from "../assets/images.svg";
import fileIcon from "../assets/file.svg";
import cameraIcon from "../assets/camera.svg";
import closeIcon from "../assets/close.svg";

const ImageUpload = ({ onImageSelect, image, onClear }) => {
  const fileRef = useRef(null);
  const cameraRef = useRef(null);

  const handleFile = (e) => {
    const file = e.target.files[0];
    if (file) {
      onImageSelect(file);
    }
  };

  return (
    <div className="upload-card">

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
              src={URL.createObjectURL(image)}
              alt="preview"
              className="preview-image"
            />
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

          <button className="btn primary" onClick={() => fileRef.current.click()}>
            <img src={fileIcon} alt="file" className="btn-icon" />
            Choose File
          </button>

          <button className="btn secondary" onClick={() => cameraRef.current.click()}>
            <img src={cameraIcon} alt="camera" className="btn-icon" />
            Take Photo
          </button>
        </div>
      )}

    </div>
  );
};

export default ImageUpload;