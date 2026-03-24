# 🚀 Production Deployment Setup

## 📋 Overview
Complete deployment configuration for Blood Cancer Classifier with:
- **Backend**: Flask API on Render
- **Frontend**: React app on Vercel  
- **Model**: Hosted on Hugging Face
- **Database**: Supabase PostgreSQL + Storage

## 🏗️ Architecture
```
User → Vercel (Frontend)
        ↓
API Calls → Render (Backend)
        ↓  
Model Download → Hugging Face
        ↓
Predictions → Supabase Database
        ↓
Images → Supabase Storage
```

## 📁 Directory Structure
```
deploy_setup/
├── backend/
│   ├── app.py              # Production Flask app
│   ├── requirements.txt       # Python dependencies
│   └── runtime.txt         # Python version
├── deployguide.txt          # Complete deployment guide
└── README.md              # This file
```

## 🚀 Quick Deploy

### 1. Backend (Render)
```bash
# Environment Variables Required:
SUPABASE_URL=...
SUPABASE_ANON_KEY=...
FRONTEND_URL=https://your-app.vercel.app
MODEL_URL=https://huggingface.co/username/repo/resolve/main/best_model.keras

# Deploy:
- Connect GitHub to Render
- Root: deploy_setup/backend/
- Build: pip install -r requirements.txt
- Start: python app.py
```

### 2. Frontend (Vercel)
```bash
# Environment Variable Required:
REACT_APP_API_URL=https://your-backend.onrender.com

# Deploy:
- Connect GitHub to Vercel
- Root: frontend/
- Build: npm run build
- Output: build/
```

### 3. Model (Hugging Face)
```bash
# Upload your trained model:
- Repository: blood-cancer-classifier
- File: best_model.keras
- Get URL from: Resolve → Download link
```

## ✅ Features
- 🤖 **Auto Model Loading** - Downloads from Hugging Face on startup
- 🔒 **Secure CORS** - Frontend-specific origin validation
- 📊 **Production Ready** - Optimized for cloud deployment
- 🗄️ **Database Integration** - Supabase connection included
- 📄 **PDF Generation** - Simple, reliable report creation
- 🏥 **Error Handling** - Graceful fallbacks and logging

## 🎯 Deployment URLs
- **Backend**: `https://your-app.onrender.com`
- **Frontend**: `https://your-app.vercel.app`
- **Model**: `https://huggingface.co/username/repo`

## 🔧 Configuration
All environment variables and settings are pre-configured for production deployment.

## 📞 Support
Check `deployguide.txt` for detailed troubleshooting and step-by-step instructions.
