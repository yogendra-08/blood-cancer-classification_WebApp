#!/usr/bin/env python3
"""
Test API endpoints
"""

import requests
import json
import time

BASE_URL = "http://localhost:5000"

def test_health():
    """Test health endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Health check passed")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_database():
    """Test database endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/test-db", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Database test passed: {data.get('status', 'unknown')}")
            return True
        else:
            print(f"❌ Database test failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Database test error: {e}")
        return False

def main():
    print("🧪 Testing API Endpoints")
    print("=" * 30)
    
    # Wait a moment for server to start
    print("⏳ Waiting for server to start...")
    time.sleep(2)
    
    # Test endpoints
    health_ok = test_health()
    db_ok = test_database()
    
    print("\n📊 Test Results:")
    print(f"   Health: {'✅' if health_ok else '❌'}")
    print(f"   Database: {'✅' if db_ok else '❌'}")
    
    if health_ok and db_ok:
        print("\n🎉 All tests passed! Your API is ready.")
    else:
        print("\n⚠️  Some tests failed. Check the server logs.")

if __name__ == '__main__':
    main()
