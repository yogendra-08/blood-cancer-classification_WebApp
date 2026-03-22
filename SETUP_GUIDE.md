# Setup Guide - Blood Cancer Classification Web App

## 🚀 Quick Setup Steps

### 1. Backend Setup

1. **Install Dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Configure Supabase**
   - Copy `env-config.txt` to `.env`
   - Update `.env` with your Supabase credentials:
     ```
     SUPABASE_URL=https://your-project-id.supabase.co
     SUPABASE_ANON_KEY=your-anon-key-here
     ```

3. **Test Supabase Connection**
   ```bash
   python test_supabase.py
   ```

4. **Start Backend Server**
   ```bash
   # Option 1: Use the production startup script (recommended)
   python start_server.py
   
   # Option 2: Direct start
   python app.py
   ```

5. **Test API Endpoints**
   ```bash
   # In a new terminal
   python test_api.py
   ```

### 2. Frontend Setup

1. **Install Dependencies**
   ```bash
   cd frontend
   npm install
   ```

2. **Start Frontend**
   ```bash
   npm start
   ```

## 🧪 Testing the Complete Flow

1. **Test Database Connection**
   - Visit: `http://localhost:5000/test-db`
   - Should return: `{"status": "connected", "data": [...]}`

2. **Test Prediction Flow**
   - Upload an image
   - Get prediction results
   - Click "Download PDF Report"
   - Fill in user details
   - Submit and download PDF

3. **Check Database**
   - Go to your Supabase dashboard
   - View the "predictions" table
   - Should see the saved record

## 🔧 Troubleshooting

### Common Issues:

1. **Supabase Connection Failed**
   - Check your `.env` file credentials
   - Verify Supabase URL and keys
   - Ensure RLS policies allow anonymous access

2. **PDF Generation Fails**
   - Check if images are saved in `backend/static/outputs/`
   - Verify GradCAM generation is working

3. **Frontend Can't Connect to Backend**
   - Update `API_BASE_URL` in `frontend/src/services/api.ts`
   - Ensure backend is running on correct port

## 📁 File Structure

```
WEB_APP/
├── backend/
│   ├── app.py              # Main Flask application
│   ├── test_supabase.py    # Database connection test
│   ├── .env                # Environment variables (create this)
│   ├── env-config.txt      # Environment template
│   └── requirements.txt    # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   └── Result.tsx  # Updated with PDF download
│   │   ├── services/
│   │   │   └── api.ts      # API service functions
│   │   └── App.tsx         # Main app with GitHub footer
│   └── package.json
├── db.txt                  # Supabase setup instructions
└── .gitignore             # Git ignore file
```

## 🎯 Features Working

✅ Image classification with EfficientNet  
✅ GradCAM visualization  
✅ Supabase database integration  
✅ User data collection form  
✅ PDF report generation  
✅ GitHub footer link  

## 📞 Support

If you encounter any issues:
1. Check the backend console logs
2. Verify Supabase table and policies
3. Test with the provided test scripts
4. Ensure all dependencies are installed
