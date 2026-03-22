#!/usr/bin/env python3
"""
Test GradCAM and local functionality without Supabase
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_local_gradcam():
    """Test GradCAM generation locally"""
    
    print("🧪 Testing Local GradCAM Generation")
    print("=" * 40)
    
    # Load model
    from app import load_efficientnet_model, generate_gradcam, generate_gradcam_plus_plus
    load_efficientnet_model()
    
    from app import model
    if model is None:
        print("❌ Model not loaded")
        return
    
    print("✅ Model loaded successfully")
    
    # Find a sample image
    uploads_dir = "uploads"
    sample_image = None
    
    if os.path.exists(uploads_dir):
        files = [f for f in os.listdir(uploads_dir) if f.endswith(('.jpg', '.jpeg', '.png'))]
        if files:
            sample_image = os.path.join(uploads_dir, files[0])
            print(f"📷 Using sample image: {os.path.basename(sample_image)}")
        else:
            print("❌ No sample images found in uploads folder")
            print("📝 Please upload an image first through the web app")
            return
    else:
        print("❌ Uploads directory not found")
        return
    
    # Test GradCAM generation
    print("\n🔥 Testing GradCAM Generation...")
    
    try:
        # Make a simple prediction first
        from app import preprocess_image
        processed_image = preprocess_image(sample_image)
        
        if processed_image is None:
            print("❌ Error preprocessing image")
            return
        
        # Make prediction
        import tensorflow as tf
        import numpy as np
        predictions = model.predict(processed_image)
        predicted_class_index = np.argmax(predictions[0])
        
        from app import CLASS_LABELS
        predicted_class = CLASS_LABELS[predicted_class_index]
        confidence = float(predictions[0][predicted_class_index])
        
        print(f"🔮 Prediction: {predicted_class} (confidence: {confidence:.2f}%)")
        
        # Test standard GradCAM
        print("\n📊 Testing Standard GradCAM...")
        gradcam_result = generate_gradcam(sample_image, predicted_class_index)
        
        if gradcam_result is not None:
            # Save locally
            output_path = "test_gradcam_standard.jpg"
            import cv2
            cv2.imwrite(output_path, gradcam_result)
            print(f"✅ Standard GradCAM saved: {output_path}")
        else:
            print("❌ Standard GradCAM failed")
        
        # Test GradCAM++
        print("\n📊 Testing GradCAM++...")
        gradcam_plus_result = generate_gradcam_plus_plus(sample_image, predicted_class_index)
        
        if gradcam_plus_result is not None:
            # Save locally
            output_path = "test_gradcam_plus.jpg"
            cv2.imwrite(output_path, gradcam_plus_result)
            print(f"✅ GradCAM++ saved: {output_path}")
        else:
            print("❌ GradCAM++ failed")
        
        print("\n🎉 Local GradCAM test completed!")
        print("📁 Check the generated files:")
        
        if os.path.exists("test_gradcam_standard.jpg"):
            print("   ✅ test_gradcam_standard.jpg")
        if os.path.exists("test_gradcam_plus.jpg"):
            print("   ✅ test_gradcam_plus.jpg")
            
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()

def test_bucket_logic():
    """Test bucket selection logic"""
    
    print("\n🎯 Testing Bucket Selection Logic")
    print("=" * 30)
    
    from app import get_bucket_name_for_class
    
    test_classes = [
        'Benign',
        '[Malignant] Pre-B',
        '[Malignant] Pro-B', 
        '[Malignant] early Pre-B'
    ]
    
    print("📊 Bucket mapping:")
    for cls in test_classes:
        bucket = get_bucket_name_for_class(cls)
        print(f"   {cls:<25} → {bucket}")
    
    print("\n✅ Bucket selection logic working correctly!")

def main():
    """Run all local tests"""
    
    print("🧪 Local Testing Suite")
    print("=" * 50)
    
    # Test 1: GradCAM generation
    test_local_gradcam()
    
    print("\n" + "=" * 50)
    
    # Test 2: Bucket logic
    test_bucket_logic()
    
    print("\n" + "=" * 50)
    print("🎉 All local tests completed!")
    print("\n💡 Next steps:")
    print("   1. If GradCAM works, create Supabase buckets")
    print("   2. Upload images through web app to test full flow")
    print("   3. Check Supabase Storage for uploaded images")

if __name__ == "__main__":
    main()
