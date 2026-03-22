#!/usr/bin/env python3
"""
Test script to verify Supabase connection and table operations
"""

import os
from dotenv import load_dotenv
from supabase import create_client

# Load environment variables
load_dotenv()

def test_supabase_connection():
    """Test Supabase database connection and table operations"""
    
    # Get Supabase credentials
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")
    
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("❌ Supabase credentials not found in .env file")
        print("Please make sure you have created a .env file with:")
        print("SUPABASE_URL=https://your-project-id.supabase.co")
        print("SUPABASE_ANON_KEY=your-anon-key-here")
        return False
    
    print(f"🔗 Connecting to Supabase at: {SUPABASE_URL}")
    
    try:
        # Create Supabase client
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        
        # Test 1: Check if table exists by trying to select data
        print("📋 Testing table access...")
        response = supabase.table('predictions').select('*').limit(1).execute()
        
        print(f"📊 Response: {response}")
        
        if hasattr(response, 'data') and response.data is not None:
            print("✅ Successfully connected to 'predictions' table")
            print(f"📊 Table has {len(response.data)} records (showing first 1)")
        else:
            print("⚠️  Table exists but no data found")
        
        # Test 2: Try to insert a test record
        print("💾 Testing insert operation...")
        test_data = {
            'name': 'Test Patient',
            'age': 30,
            'gender': 'Male',
            'mobile': '1234567890',
            'predicted_class': 'Benign',
            'confidence': 85.5,
            'input_image_url': 'test_input.jpg',
            'gradcam_image_url': 'test_gradcam.jpg'
        }
        
        insert_response = supabase.table('predictions').insert(test_data).execute()
        
        if insert_response.data:
            print("✅ Successfully inserted test record")
            test_id = insert_response.data[0]['id']
            print(f"🆔 Test record ID: {test_id}")
            
            # Test 3: Delete the test record
            print("🗑️  Cleaning up test record...")
            delete_response = supabase.table('predictions').delete().eq('id', test_id).execute()
            
            if delete_response.data:
                print("✅ Successfully deleted test record")
            else:
                print("⚠️  Could not delete test record")
        else:
            print("❌ Failed to insert test record")
            print(f"Insert response: {insert_response}")
            return False
        
        print("\n🎉 All tests passed! Supabase is properly configured.")
        return True
        
    except Exception as e:
        print(f"❌ Error connecting to Supabase: {str(e)}")
        print("\n🔧 Troubleshooting:")
        print("1. Check if your Supabase URL is correct")
        print("2. Verify your anon key is valid")
        print("3. Make sure the 'predictions' table exists")
        print("4. Check RLS policies allow anonymous access")
        return False

if __name__ == "__main__":
    print("🧪 Testing Supabase Connection")
    print("=" * 40)
    
    success = test_supabase_connection()
    
    if success:
        print("\n✅ Your backend is ready to use Supabase!")
    else:
        print("\n❌ Please fix the issues above before proceeding.")
