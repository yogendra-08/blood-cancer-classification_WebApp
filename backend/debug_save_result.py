#!/usr/bin/env python3
"""
Debug save-result endpoint step by step
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def debug_save_result():
    """Debug the save-result process"""
    
    print("🔍 Debugging Save-Result Process")
    print("=" * 50)
    
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
        
        # Simulate the save-result request data
        print("\n📋 Simulating save-result request...")
        
        # Test 1: Check uploads directory
        uploads_dir = "uploads"
        if os.path.exists(uploads_dir):
            files = [f for f in os.listdir(uploads_dir) if f.endswith(('.jpg', '.jpeg', '.png'))]
            print(f"📁 Files in uploads: {len(files)}")
            for f in files[:3]:  # Show first 3 files
                print(f"   - {f}")
        else:
            print("❌ Uploads directory not found")
            return
        
        # Test 2: Check static/outputs directory
        outputs_dir = "static/outputs"
        if os.path.exists(outputs_dir):
            files = [f for f in os.listdir(outputs_dir) if f.endswith(('.jpg', '.jpeg', '.png'))]
            print(f"🎨 Files in outputs: {len(files)}")
            for f in files[:3]:  # Show first 3 files
                print(f"   - {f}")
        else:
            print("❌ Outputs directory not found")
            return
        
        # Test 3: Check database connection
        print("\n🗄️ Testing database connection...")
        try:
            response = supabase.table('predictions').select('*').limit(1).execute()
            if response.data:
                print(f"✅ Database connected, {len(response.data)} records found")
                for record in response.data:
                    print(f"   - ID: {record.get('id')}, Class: {record.get('predicted_class')}")
            else:
                print("✅ Database connected, no records found")
        except Exception as e:
            print(f"❌ Database connection error: {e}")
        
        # Test 4: Check if buckets exist (basic check)
        print("\n🪣 Testing bucket access...")
        try:
            # Try to list buckets (this might fail depending on permissions)
            buckets = supabase.storage.list_buckets()
            print("✅ Buckets found:")
            for bucket in buckets:
                print(f"   - {bucket.name}")
        except Exception as e:
            print(f"⚠️  Could not list buckets: {e}")
            print("   This is normal if you don't have admin permissions")
        
        print("\n🎉 Debug completed!")
        print("\n💡 Next steps:")
        print("   1. Create 4 buckets in Supabase if not created")
        print("   2. Test upload through web app")
        print("   3. Check server logs for detailed info")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_save_result()
