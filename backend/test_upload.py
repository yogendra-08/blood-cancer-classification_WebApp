#!/usr/bin/env python3
"""
Test actual upload to Supabase Storage
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_upload():
    """Test uploading a sample image to Supabase"""
    
    print("🧪 Testing Upload to Supabase Storage")
    print("=" * 40)
    
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
        
        # Import upload function
        from app import upload_image_to_supabase, get_bucket_name_for_class
        
        # Test upload to each bucket
        uploads_dir = "uploads"
        if os.path.exists(uploads_dir):
            files = [f for f in os.listdir(uploads_dir) if f.endswith(('.jpg', '.jpeg', '.png'))]
            if files:
                test_image = os.path.join(uploads_dir, files[0])
                print(f"📷 Testing with: {os.path.basename(test_image)}")
                
                # Test upload to benign-images
                print("\n📊 Testing upload to benign-images...")
                result_url = upload_image_to_supabase(test_image, "benign-images")
                if result_url:
                    print(f"✅ Success: {result_url}")
                else:
                    print("❌ Failed")
                
                # Test upload to malignant-preb-images
                print("\n📊 Testing upload to malignant-preb-images...")
                result_url = upload_image_to_supabase(test_image, "malignant-preb-images")
                if result_url:
                    print(f"✅ Success: {result_url}")
                else:
                    print("❌ Failed")
                    
        else:
            print("❌ No test images found")
            return
        
        print("\n🎉 Upload test completed!")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_upload()
