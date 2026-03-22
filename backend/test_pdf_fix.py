#!/usr/bin/env python3
"""
Test PDF generation fix
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_pdf_generation():
    """Test both PDF generation methods"""
    
    print("🧪 Testing PDF Generation Fix")
    print("=" * 40)
    
    try:
        from app import generate_pdf_report, generate_simple_pdf
        
        # Sample data
        user_data = {
            'name': 'Test Patient',
            'age': 30,
            'gender': 'Male',
            'mobile': '1234567890'
        }
        
        prediction_data = {
            'class': '[Malignant] early Pre-B',
            'confidence': 92.5
        }
        
        # Test 1: Simple PDF (should always work)
        print("\n📄 Testing Simple PDF Generation...")
        simple_pdf = generate_simple_pdf(user_data, prediction_data)
        
        if simple_pdf:
            with open('test_simple.pdf', 'wb') as f:
                f.write(simple_pdf)
            print("✅ Simple PDF generated: test_simple.pdf")
        else:
            print("❌ Simple PDF failed")
        
        # Test 2: Full PDF with images (if available)
        print("\n📄 Testing Full PDF Generation...")
        
        # Find sample images
        uploads_dir = "uploads"
        outputs_dir = "static/outputs"
        
        input_image = None
        gradcam_image = None
        
        if os.path.exists(uploads_dir):
            files = [f for f in os.listdir(uploads_dir) if f.endswith(('.jpg', '.jpeg', '.png'))]
            if files:
                input_image = os.path.join(uploads_dir, files[0])
                print(f"📷 Using input image: {os.path.basename(input_image)}")
        
        if os.path.exists(outputs_dir):
            files = [f for f in os.listdir(outputs_dir) if f.endswith(('.jpg', '.jpeg', '.png'))]
            if files:
                gradcam_image = os.path.join(outputs_dir, files[0])
                print(f"🎨 Using GradCAM image: {os.path.basename(gradcam_image)}")
        
        # Try full PDF
        full_pdf = generate_pdf_report(user_data, prediction_data, input_image, gradcam_image)
        
        if full_pdf:
            with open('test_full.pdf', 'wb') as f:
                f.write(full_pdf)
            print("✅ Full PDF generated: test_full.pdf")
        else:
            print("❌ Full PDF failed (but fallback should work)")
        
        print("\n🎉 PDF testing completed!")
        print("📁 Check generated files:")
        
        if os.path.exists('test_simple.pdf'):
            print("   ✅ test_simple.pdf")
        if os.path.exists('test_full.pdf'):
            print("   ✅ test_full.pdf")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_pdf_generation()
