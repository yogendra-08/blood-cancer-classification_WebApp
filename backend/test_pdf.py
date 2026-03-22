#!/usr/bin/env python3
"""
Test PDF generation functionality
"""

import os
import sys
from datetime import datetime

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import generate_pdf_report

def test_pdf_generation():
    """Test PDF generation with sample data"""
    
    # Sample user data
    user_data = {
        'name': 'Test Patient',
        'age': 30,
        'gender': 'Male',
        'mobile': '1234567890'
    }
    
    # Sample prediction data
    prediction_data = {
        'class': 'Benign',
        'confidence': 85.5
    }
    
    # Test without images first
    print("🧪 Testing PDF generation without images...")
    try:
        pdf_content = generate_pdf_report(user_data, prediction_data, None, None)
        
        if pdf_content:
            # Save test PDF
            with open('test_output.pdf', 'wb') as f:
                f.write(pdf_content)
            print("✅ PDF generated successfully without images")
            print("📄 Saved as: test_output.pdf")
            return True
        else:
            print("❌ PDF generation failed")
            return False
            
    except Exception as e:
        print(f"❌ PDF generation error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_pdf_with_images():
    """Test PDF generation with images if available"""
    
    # Check for sample images
    uploads_dir = 'uploads'
    outputs_dir = 'static/outputs'
    
    input_image = None
    gradcam_image = None
    
    # Find sample images
    if os.path.exists(uploads_dir):
        files = [f for f in os.listdir(uploads_dir) if f.endswith(('.jpg', '.jpeg', '.png'))]
        if files:
            input_image = os.path.join(uploads_dir, files[0])
            print(f"📷 Using input image: {input_image}")
    
    if os.path.exists(outputs_dir):
        files = [f for f in os.listdir(outputs_dir) if f.endswith(('.jpg', '.jpeg', '.png'))]
        if files:
            gradcam_image = os.path.join(outputs_dir, files[0])
            print(f"🎨 Using GradCAM image: {gradcam_image}")
    
    if not input_image and not gradcam_image:
        print("⚠️  No sample images found, skipping image test")
        return True
    
    # Sample data
    user_data = {
        'name': 'Test Patient with Images',
        'age': 25,
        'gender': 'Female',
        'mobile': '9876543210'
    }
    
    prediction_data = {
        'class': '[Malignant] Pre-B',
        'confidence': 92.3
    }
    
    print("🧪 Testing PDF generation with images...")
    try:
        pdf_content = generate_pdf_report(user_data, prediction_data, input_image, gradcam_image)
        
        if pdf_content:
            # Save test PDF
            with open('test_output_with_images.pdf', 'wb') as f:
                f.write(pdf_content)
            print("✅ PDF generated successfully with images")
            print("📄 Saved as: test_output_with_images.pdf")
            return True
        else:
            print("❌ PDF generation with images failed")
            return False
            
    except Exception as e:
        print(f"❌ PDF generation error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("🧪 Testing PDF Generation")
    print("=" * 30)
    
    # Test 1: PDF without images
    test1_ok = test_pdf_generation()
    
    print("\n" + "=" * 30)
    
    # Test 2: PDF with images (if available)
    test2_ok = test_pdf_with_images()
    
    print("\n📊 Test Results:")
    print(f"   PDF without images: {'✅' if test1_ok else '❌'}")
    print(f"   PDF with images: {'✅' if test2_ok else '❌'}")
    
    if test1_ok and test2_ok:
        print("\n🎉 All PDF tests passed!")
    else:
        print("\n⚠️  Some PDF tests failed.")

if __name__ == '__main__':
    main()
