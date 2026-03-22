# Blood Cancer Classification Web App 🩸

A comprehensive web application for blood cancer classification using deep learning with GradCAM visualization and Supabase integration.

## 🎯 Features

- **AI-Powered Classification**: Classifies blood cancer into 4 categories
- **GradCAM Visualization**: Shows model's focus areas on medical images
- **Supabase Integration**: Cloud storage and database
- **PDF Reports**: Professional medical reports with patient data
- **Class-Specific Storage**: Images organized by prediction class
- **Responsive Design**: Works on desktop and mobile
- **Real-time Processing**: Fast predictions with confidence scores

## 🏗️ Architecture

### Backend (Flask + TensorFlow)
- **Model**: EfficientNet for blood cancer classification
- **Classes**: Benign, [Malignant] Pre-B, [Malignant] Pro-B, [Malignant] early Pre-B
- **Database**: Supabase PostgreSQL
- **Storage**: Supabase Storage (4 class-specific buckets)
- **PDF Generation**: ReportLab for medical reports

### Frontend (React + TypeScript)
- **UI**: Modern, responsive interface
- **File Upload**: Drag-and-drop image upload
- **Results Display**: Classification with confidence scores
- **GradCAM Visualization**: Interactive heatmap overlay
- **Patient Forms**: Data collection for reports
- **PDF Download**: One-click report generation

## 🚀 Quick Start

### Prerequisites
- Node.js 16+
- Python 3.8+
- Supabase account
- Git

### Installation

1. **Clone Repository**
   ```bash
   git clone https://github.com/yogendra-08/blood-cancer-classification_WebApp.git
   cd blood-cancer-classification_WebApp
   ```

2. **Backend Setup**
   ```bash
   cd backend
   pip install -r requirements.txt
   cp .env.example .env
   # Edit .env with your Supabase credentials
   ```

3. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   ```

4. **Supabase Setup**
   - Create 4 storage buckets: `benign-images`, `malignant-preb-images`, `malignant-prob-images`, `malignant-early-preb-images`
   - Set up public access policies
   - Update CORS settings

### Local Development

1. **Start Backend**
   ```bash
   cd backend
   python app.py
   ```

2. **Start Frontend**
   ```bash
   cd frontend
   npm start
   ```

3. **Access Application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:5000

## 🌐 Deployment

### Backend (Render)
```bash
# Environment Variables
SUPABASE_URL=your_supabase_url
SUPABASE_ANON_KEY=your_supabase_anon_key
SUPABASE_SERVICE_KEY=your_supabase_service_key

# Start Command
python app.py
```

### Frontend (Vercel/Netlify)
```bash
# Build Command
npm run build

# Environment Variables (Optional)
REACT_APP_API_URL=your_backend_url

# Publish Directory
build/
```

## 📊 Supabase Storage Structure

```
benign-images/              # Benign class predictions
malignant-preb-images/       # [Malignant] Pre-B predictions  
malignant-prob-images/        # [Malignant] Pro-B predictions
malignant-early-preb-images/ # [Malignant] early Pre-B predictions
```

## 🔧 API Endpoints

### POST /predict
- **Purpose**: Classify uploaded blood cell images
- **Input**: Image file (multipart/form-data)
- **Output**: JSON with prediction and GradCAM URL

### POST /save-result
- **Purpose**: Save patient data and generate PDF report
- **Input**: Form data with patient details
- **Output**: PDF download and database storage

### GET /health
- **Purpose**: Health check endpoint
- **Output**: Server status and model info

### GET /test-db
- **Purpose**: Test Supabase connection
- **Output**: Database connection status

## 🎨 Model Information

- **Architecture**: EfficientNet-B0
- **Input Size**: 224x224 RGB images
- **Classes**: 4 blood cancer categories
- **Training**: Medical imaging dataset
- **GradCAM**: Layer-wise activation visualization

## 📄 PDF Reports

Generated reports include:
- Patient information (name, age, gender, mobile)
- Classification results with confidence scores
- Original blood cell image
- GradCAM visualization heatmap
- Timestamp and metadata

## 🔒 Security Features

- **Environment Variables**: Sensitive data in .env
- **Input Validation**: File type and size limits
- **CORS Configuration**: Secure cross-origin requests
- **Supabase Policies**: Row-level security

## 🧪 Testing

### Backend Tests
```bash
cd backend
python test_supabase.py      # Test database connection
python test_upload.py        # Test image upload
python test_pdf_fix.py       # Test PDF generation
```

### Frontend Tests
```bash
cd frontend
npm test                 # Run unit tests
npm run build           # Test production build
```

## 📈 Performance

- **Prediction Time**: < 3 seconds
- **Accuracy**: Medical-grade classification
- **Memory Usage**: Optimized for production
- **Concurrent Users**: Threaded Flask server

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Support

For issues and questions:
- 📧 Email: [your-email@example.com]
- 🐛 Issues: [GitHub Issues](https://github.com/yogendra-08/blood-cancer-classification_WebApp/issues)
- 📚 Documentation: [Wiki](https://github.com/yogendra-08/blood-cancer-classification_WebApp/wiki)

## 🌟 Acknowledgments

- **TensorFlow/Keras**: Deep learning framework
- **EfficientNet**: Model architecture
- **Supabase**: Backend services
- **ReportLab**: PDF generation
- **OpenCV**: Image processing
- **React**: Frontend framework

---

**Built with ❤️ for medical AI applications** 🩸✨
