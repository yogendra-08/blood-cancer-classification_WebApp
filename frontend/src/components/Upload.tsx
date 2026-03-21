import React, { useState, useRef } from 'react';
import { uploadImage, PredictionResult } from '../services/api';

interface UploadProps {
  onPrediction: (result: PredictionResult) => void;
  onLoading: (loading: boolean) => void;
  onError: (error: string) => void;
  loading: boolean;
  hasResult: boolean;
  onReset: () => void;
}

const Upload: React.FC<UploadProps> = ({
  onPrediction,
  onLoading,
  onError,
  loading,
  hasResult,
  onReset
}) => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [isDragging, setIsDragging] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileSelect = (file: File) => {
    if (file && file.type.startsWith('image/')) {
      setSelectedFile(file);
      const url = URL.createObjectURL(file);
      setPreviewUrl(url);
      onError('');
    } else {
      onError('Please select a valid image file');
    }
  };

  const handleFileInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      handleFileSelect(file);
    }
  };

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(false);
    
    const file = e.dataTransfer.files[0];
    if (file) {
      handleFileSelect(file);
    }
  };

  const handleDragOver = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handlePredict = async () => {
    if (!selectedFile) {
      onError('Please select an image first');
      return;
    }

    onLoading(true);
    
    try {
      const result = await uploadImage(selectedFile);
      onPrediction(result);
    } catch (error) {
      onError(error instanceof Error ? error.message : 'Failed to process image');
    }
  };

  const handleResetUpload = () => {
    setSelectedFile(null);
    setPreviewUrl(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
    onReset();
  };

  const handleClick = () => {
    if (fileInputRef.current) {
      fileInputRef.current.click();
    }
  };

  return (
    <div className="upload-section">
      <div
        className={`upload-area ${isDragging ? 'dragover' : ''}`}
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onClick={handleClick}
      >
        <input
          ref={fileInputRef}
          type="file"
          className="file-input"
          accept="image/*"
          onChange={handleFileInputChange}
          disabled={loading}
        />
        
        <div className="upload-icon">📷</div>
        <div className="upload-text">
          {selectedFile ? selectedFile.name : 'Click to upload or drag and drop'}
        </div>
        <div className="upload-hint">
          Supported formats: PNG, JPG, JPEG, GIF, BMP, TIFF
        </div>
      </div>

      {previewUrl && (
        <div className={`preview-section ${previewUrl ? 'active' : ''}`}>
          <h3>Image Preview</h3>
          <img
            src={previewUrl}
            alt="Preview"
            className="preview-image"
          />
          <div style={{ display: 'flex', gap: '10px', justifyContent: 'center', marginTop: '20px' }}>
            <button
              className="predict-button"
              onClick={handlePredict}
              disabled={loading}
            >
              {loading ? 'Analyzing...' : 'Predict Cancer Type'}
            </button>
            {hasResult && (
              <button
                className="predict-button"
                onClick={handleResetUpload}
                disabled={loading}
                style={{ background: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)' }}
              >
                Upload New Image
              </button>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default Upload;
