#!/usr/bin/env python3
"""
Blood Cancer Classification Backend - Production Ready
Deployed on Render with Hugging Face Model Integration
"""

import os
import uuid
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.efficientnet import preprocess_input
import cv2
import requests
import tempfile
import base64
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
import io
from supabase import create_client, Client

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__, static_folder='static', static_url_path='/static')

# Enable CORS for all routes with frontend URL
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")
CORS(app, resources={r"/api/*": {"origins": [FRONTEND_URL]}})

# Supabase configuration
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://your-project-id.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY", "your-anon-key-here")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Configuration
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'static/outputs'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Class labels
CLASS_LABELS = ['Benign', '[Malignant] Pre-B', '[Malignant] Pro-B', '[Malignant] early Pre-B']

# Model variables
model = None
MODEL_URL = os.getenv("MODEL_URL", "https://huggingface.co/your-username/blood-cancer-model/resolve/main/best_model.keras")

def load_model_from_huggingface():
    """Load model from Hugging Face repository"""
    global model
    
    if model is not None:
        print("✅ Model already loaded")
        return model
    
    try:
        print(f"🔄 Loading model from Hugging Face: {MODEL_URL}")
        
        # Download model if not exists
        model_path = "best_model.keras"
        if not os.path.exists(model_path):
            print("📥 Downloading model from Hugging Face...")
            response = requests.get(MODEL_URL)
            if response.status_code == 200:
                with open(model_path, 'wb') as f:
                    f.write(response.content)
                print("✅ Model downloaded successfully")
            else:
                print(f"❌ Failed to download model: {response.status_code}")
                return None
        
        # Load the model
        if os.path.exists(model_path):
            model = tf.keras.models.load_model(model_path)
            print("✅ Model loaded successfully from Hugging Face")
            return model
        else:
            print("❌ Model file not found")
            return None
            
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return None

def preprocess_image(img_path):
    """Preprocess image for model input"""
    try:
        img = image.load_img(img_path, target_size=(224, 224))
        img_array = image.img_to_array(img)
        # Expand dimensions to match model input shape
        img_array = np.expand_dims(img_array, axis=0)
        # Preprocess using EfficientNet preprocessing
        img_array = preprocess_input(img_array)
        return img_array
    except Exception as e:
        print(f"Error preprocessing image: {e}")
        return None

def get_bucket_name_for_class(predicted_class):
    """Get appropriate bucket name based on predicted class"""
    class_to_bucket = {
        'Benign': 'benign-images',
        '[Malignant] Pre-B': 'malignant-preb-images',
        '[Malignant] Pro-B': 'malignant-prob-images', 
        '[Malignant] early Pre-B': 'malignant-early-preb-images'
    }
    return class_to_bucket.get(predicted_class, 'unknown-images')

def upload_image_to_supabase(image_path, bucket_name="predictions"):
    """Upload image to Supabase Storage"""
    try:
        # Read image file
        with open(image_path, 'rb') as f:
            image_data = f.read()
        
        # Generate unique filename
        filename = f"{uuid.uuid4()}_{os.path.basename(image_path)}"
        
        # Upload to Supabase Storage
        response = supabase.storage.from_(bucket_name).upload(
            path=filename,
            file=image_data,
            file_options={"content-type": "image/jpeg"}
        )
        
        if response.data:
            # Get public URL
            public_url = supabase.storage.from_(bucket_name).get_public_url(filename)
            print(f"✅ Image uploaded to Supabase: {public_url}")
            return public_url
        else:
            print(f"❌ Upload failed: {response}")
            return None
            
    except Exception as e:
        print(f"❌ Error uploading to Supabase: {e}")
        return None

def generate_simple_pdf(user_data, prediction_data):
    """Generate simple PDF without images"""
    try:
        # Create PDF buffer
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter
        
        # Title
        p.setFont("Helvetica-Bold", 16)
        p.drawString(50, height - 50, "Blood Cancer Classification Report")
        
        # Patient Information
        p.setFont("Helvetica-Bold", 12)
        p.drawString(50, height - 100, "Patient Information:")
        p.setFont("Helvetica", 10)
        y_position = height - 120
        
        p.drawString(70, y_position, f"Name: {user_data.get('name', 'N/A')}")
        y_position -= 20
        p.drawString(70, y_position, f"Age: {user_data.get('age', 'N/A')}")
        y_position -= 20
        p.drawString(70, y_position, f"Gender: {user_data.get('gender', 'N/A')}")
        y_position -= 20
        p.drawString(70, y_position, f"Mobile: {user_data.get('mobile', 'N/A')}")
        y_position -= 40
        
        # Prediction Results
        p.setFont("Helvetica-Bold", 12)
        p.drawString(50, y_position, "Prediction Results:")
        p.setFont("Helvetica", 10)
        y_position -= 20
        
        p.drawString(70, y_position, f"Predicted Class: {prediction_data.get('class', 'N/A')}")
        y_position -= 20
        p.drawString(70, y_position, f"Confidence: {prediction_data.get('confidence', 0):.2f}%")
        y_position -= 40
        
        # Note about images
        p.setFont("Helvetica", 9)
        p.drawString(50, y_position, "Note: Images were not available for this report.")
        y_position -= 20
        p.drawString(50, y_position, "Please check the web application for visual analysis.")
        
        # Footer
        p.setFont("Helvetica", 8)
        p.drawString(width - 200, 30, "Blood Cancer Classification Web App")
        p.drawString(width - 200, 20, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Save PDF
        p.save()
        buffer.seek(0)
        
        print("✅ Simple PDF generated successfully")
        return buffer.getvalue()
    except Exception as e:
        print(f"❌ Error generating simple PDF: {e}")
        return None

# Load model on startup
load_model_from_huggingface()

@app.route('/predict', methods=['POST'])
def predict():
    """Predict blood cancer class from uploaded image"""
    try:
        if model is None:
            return jsonify({'error': 'Model not loaded'}), 500
        
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Generate unique filename
        unique_filename = f"{uuid.uuid4()}_{file.filename}"
        upload_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        
        # Save uploaded file
        file.save(upload_path)
        print(f"File uploaded: {upload_path}")
        
        # Preprocess image
        processed_image = preprocess_image(upload_path)
        if processed_image is None:
            return jsonify({'error': 'Error preprocessing image'}), 500
        
        # Make prediction
        predictions = model.predict(processed_image)
        predicted_class_index = np.argmax(predictions[0])
        predicted_class = CLASS_LABELS[predicted_class_index]
        confidence = float(predictions[0][predicted_class_index])
        
        # Return results
        response = {
            'success': True,
            'prediction': {
                'class': predicted_class,
                'confidence': round(confidence * 100, 2),
                'all_probabilities': {
                    CLASS_LABELS[i]: round(float(predictions[0][i]) * 100, 2) 
                    for i in range(len(CLASS_LABELS))
                }
            },
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(response)
        
    except Exception as e:
        print(f"Error in prediction: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/save-result', methods=['POST'])
def save_result():
    """Save prediction results to database and generate PDF"""
    try:
        # Get form data
        user_data = {
            'name': request.form.get('name', ''),
            'age': int(request.form.get('age', 0)) if request.form.get('age') else None,
            'gender': request.form.get('gender', ''),
            'mobile': request.form.get('mobile', '')
        }
        
        # Get prediction data
        prediction_data = {
            'class': request.form.get('predicted_class', ''),
            'confidence': float(request.form.get('confidence', 0))
        }
        
        # Validate required fields
        if not all([user_data['name'], user_data['age'], user_data['gender'], 
                   user_data['mobile'], prediction_data['class']]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Save to Supabase
        db_data = {
            'name': user_data['name'],
            'age': user_data['age'],
            'gender': user_data['gender'],
            'mobile': user_data['mobile'],
            'predicted_class': prediction_data['class'],
            'confidence': prediction_data['confidence'],
            'input_image_url': '',
            'gradcam_image_url': ''
        }
        
        response = supabase.table('predictions').insert(db_data).execute()
        
        if not response.data:
            return jsonify({'error': 'Failed to save to database'}), 500
        
        # Generate PDF
        pdf_content = generate_simple_pdf(user_data, prediction_data)
        
        if pdf_content:
            # Encode PDF for response
            pdf_base64 = base64.b64encode(pdf_content).decode('utf-8')
            
            return jsonify({
                'success': True,
                'message': 'Report generated successfully',
                'pdf_content': pdf_base64,
                'database_id': response.data[0]['id']
            })
        else:
            return jsonify({
                'success': False,
                'message': 'PDF generation failed',
                'database_id': response.data[0]['id']
            })
        
    except Exception as e:
        print(f"Error saving result: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None,
        'model_source': 'Hugging Face',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/test-db', methods=['GET'])
def test_db():
    """Test Supabase database connection"""
    try:
        response = supabase.table('predictions').select('*').limit(1).execute()
        return jsonify({"status": "connected", "data": response.data})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/static/outputs/<filename>')
def serve_gradcam(filename):
    """Serve GradCAM output images"""
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename)

if __name__ == '__main__':
    # Suppress TensorFlow warnings
    os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
    
    print("🚀 Starting Blood Cancer Classification API...")
    print("📥 Loading model from Hugging Face...")
    load_model_from_huggingface()
    print(f"✅ Model ready: {model is not None}")
    
    # Run on all interfaces for deployment
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
