#!/usr/bin/env python3
"""
Production-ready server startup script
"""

import os
import sys
import warnings

# Suppress all warnings
warnings.filterwarnings('ignore')
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

# Import and run the app
from app import app, load_efficientnet_model

def main():
    print("🚀 Starting Blood Cancer Classification API...")
    print("📦 Loading model...")
    
    # Load model
    load_efficientnet_model()
    
    print("✅ Server ready!")
    print("📡 API Endpoints:")
    print("   - GET  /health")
    print("   - POST /predict")
    print("   - POST /save-result")
    print("   - GET  /test-db")
    print("🌐 Server running on: http://localhost:5000")
    
    # Run production server
    try:
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=False,
            threaded=True
        )
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Server error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
