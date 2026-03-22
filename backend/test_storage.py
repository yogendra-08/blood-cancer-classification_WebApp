#!/usr/bin/env python3
"""
Test Supabase Storage upload functionality
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_supabase_storage():
    """Test uploading to Supabase Storage"""
    
    # Get Supabase credentials
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")
    
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("❌ Missing Supabase credentials")
        return
    
    try:
        from supabase import create_client
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("✅ Supabase client created")
        
        # Check if we have a test image
        uploads_dir = "uploads"
        test_image = None
        
        if os.path.exists(uploads_dir):
            files = [f for f in os.listdir(uploads_dir) if f.endswith(('.jpg', '.jpeg', '.png'))]
            if files:
                test_image = os.path.join(uploads_dir, files[0])
                print(f"📷 Using test image: {test_image}")
            else:
                print("❌ No test images found in uploads folder")
                return
        else:
            print("❌ Uploads folder not found")
            return
        
        # Test upload to input-images bucket
        print("\n🧪 Testing upload to 'input-images' bucket...")
        
        # Import the upload function
        from app import upload_image_to_supabase
        
        # Try upload
        result_url = upload_image_to_supabase(test_image, "input-images")
        
        if result_url:
            print(f"✅ Upload successful!")
            print(f"🌐 Public URL: {result_url}")
            
            # Test if URL is accessible
            try:
                import requests
                response = requests.head(result_url, timeout=10)
                if response.status_code == 200:
                    print("✅ URL is accessible")
                else:
                    print(f"⚠️  URL returned status: {response.status_code}")
            except Exception as e:
                print(f"⚠️  Could not test URL accessibility: {e}")
        else:
            print("❌ Upload failed")
            
        # Test upload to gradcam-images bucket
        print("\n🧪 Testing upload to 'gradcam-images' bucket...")
        gradcam_result_url = upload_image_to_supabase(test_image, "gradcam-images")
        
        if gradcam_result_url:
            print(f"✅ GradCAM upload successful!")
            print(f"🌐 GradCAM URL: {gradcam_result_url}")
        else:
            print("❌ GradCAM upload failed")
        
        print("\n🎉 Storage test completed!")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

def check_buckets():
    """Check if buckets exist"""
    try:
        from supabase import create_client
        supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_ANON_KEY"))
        
        print("\n🔍 Checking buckets...")
        
        # Try to list buckets (this might fail depending on permissions)
        try:
            buckets = supabase.storage.list_buckets()
            print("✅ Buckets found:")
            for bucket in buckets:
                print(f"   - {bucket.name}")
        except Exception as e:
            print(f"⚠️  Could not list buckets: {e}")
            print("   This is normal if you don't have admin permissions")
            print("   Please check manually in Supabase Dashboard")
        
    except Exception as e:
        print(f"❌ Error checking buckets: {e}")

if __name__ == "__main__":
    print("🧪 Testing Supabase Storage")
    print("=" * 30)
    
    # Check buckets first
    check_buckets()
    
    # Test upload
    test_supabase_storage()
