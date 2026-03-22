#!/usr/bin/env python3
"""
Debug GradCAM generation step by step
"""

import os
import numpy as np
import cv2
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.efficientnet import preprocess_input
import tensorflow as tf

# Import the model loading function
from app import load_efficientnet_model

def debug_gradcam():
    """Debug GradCAM generation"""
    
    print("🔍 Debugging GradCAM Generation")
    print("=" * 40)
    
    # Load model
    print("📦 Loading model...")
    load_efficientnet_model()
    
    # Check if model exists
    from app import model
    if model is None:
        print("❌ Model not loaded")
        return
    
    print(f"✅ Model loaded: {type(model)}")
    print(f"📊 Input shape: {model.input_shape}")
    print(f"📊 Output shape: {model.output_shape}")
    
    # Print model layers
    print("\n🔍 Model Layers:")
    conv_layers = []
    for i, layer in enumerate(model.layers):
        if isinstance(layer, tf.keras.layers.Conv2D):
            conv_layers.append((i, layer.name, layer.output.shape))
            print(f"   {i}: {layer.name} - {layer.output.shape}")
    
    if not conv_layers:
        print("❌ No convolutional layers found!")
        return
    
    print(f"\n✅ Found {len(conv_layers)} conv layers")
    
    # Find a sample image
    uploads_dir = "uploads"
    sample_image = None
    
    if os.path.exists(uploads_dir):
        files = [f for f in os.listdir(uploads_dir) if f.endswith(('.jpg', '.jpeg', '.png'))]
        if files:
            sample_image = os.path.join(uploads_dir, files[0])
            print(f"📷 Using sample image: {sample_image}")
        else:
            print("❌ No sample images found")
            return
    else:
        print("❌ Uploads directory not found")
        return
    
    # Test GradCAM step by step
    print("\n🧪 Testing GradCAM Generation...")
    
    try:
        # Load and preprocess image
        print("📥 Loading image...")
        img = image.load_img(sample_image, target_size=(224, 224))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)
        print(f"✅ Image preprocessed: {img_array.shape}")
        
        # Make prediction
        print("🔮 Making prediction...")
        predictions = model.predict(img_array)
        predicted_class_index = np.argmax(predictions[0])
        confidence = float(predictions[0][predicted_class_index])
        print(f"✅ Prediction: class {predicted_class_index}, confidence {confidence:.2f}")
        
        # Test with the best conv layer using new logic
        suitable_conv_layers = []
        for i, layer in enumerate(model.layers):
            if isinstance(layer, tf.keras.layers.Conv2D):
                output_shape = layer.output.shape
                # Only include layers with reasonable spatial dimensions (at least 7x7)
                if len(output_shape) >= 3 and output_shape[1] >= 7 and output_shape[2] >= 7:
                    suitable_conv_layers.append((i, layer.name, output_shape))
        
        if not suitable_conv_layers:
            print("❌ No suitable convolutional layers found!")
            return
        
        print(f"\n✅ Found {len(suitable_conv_layers)} suitable conv layers:")
        for i, name, shape in suitable_conv_layers:
            print(f"   {i}: {name} - {shape}")
        
        # Use a layer with good spatial dimensions (prefer 14x14 or 28x28)
        best_layer_name = None
        for i, name, shape in suitable_conv_layers:
            if shape[1] == 14 and shape[2] == 14:
                best_layer_name = name
                break
        
        if best_layer_name is None:
            # Fallback to the largest layer
            best_layer_name = suitable_conv_layers[0][1]
        
        print(f"\n🎯 Using layer: {best_layer_name}")
        
        # Create grad model
        print("🔧 Creating gradient model...")
        grad_model = tf.keras.models.Model(
            [model.input], 
            [model.get_layer(best_layer_name).output, model.output]
        )
        print("✅ Gradient model created")
        
        # Test gradient computation
        print("🌊 Computing gradients...")
        with tf.GradientTape() as tape:
            conv_outputs, predictions = grad_model(img_array)
            if isinstance(predictions, list):
                predictions = predictions[0]
            tape.watch(conv_outputs)
            loss = predictions[:, predicted_class_index]
        
        print(f"✅ Loss computed: {loss.numpy()}")
        print(f"📊 Conv outputs shape: {conv_outputs.shape}")
        
        # Get gradients
        grads = tape.gradient(loss, conv_outputs)
        
        if grads is None:
            print("❌ Gradients are None!")
            print("🔍 This is the problem - gradients are not flowing")
            return
        else:
            print(f"✅ Gradients computed: {grads.shape}")
            print(f"📊 Gradient range: [{grads.numpy().min():.6f}, {grads.numpy().max():.6f}]")
        
        # Continue with heatmap generation
        print("🔥 Generating heatmap...")
        pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
        last_conv_layer_output = conv_outputs[0]
        heatmap = tf.multiply(last_conv_layer_output, pooled_grads)
        heatmap = tf.reduce_mean(heatmap, axis=-1)
        heatmap = tf.squeeze(heatmap)
        
        # Normalize
        heatmap = tf.maximum(heatmap, 0) / (tf.math.reduce_max(heatmap) + 1e-8)
        heatmap = heatmap.numpy()
        
        print(f"✅ Heatmap generated: {heatmap.shape}")
        print(f"📊 Heatmap range: [{heatmap.min():.6f}, {heatmap.max():.6f}]")
        
        # Create visualization
        print("🎨 Creating visualization...")
        original_img = cv2.imread(sample_image)
        original_img = cv2.resize(original_img, (224, 224))
        
        heatmap = cv2.resize(heatmap, (original_img.shape[1], original_img.shape[0]))
        heatmap = np.uint8(255 * heatmap)
        heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
        superimposed_img = cv2.addWeighted(original_img, 0.6, heatmap, 0.4, 0)
        
        # Save result
        output_path = "debug_gradcam_result.jpg"
        cv2.imwrite(output_path, superimposed_img)
        print(f"✅ GradCAM saved: {output_path}")
        
        print("\n🎉 GradCAM generation successful!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_gradcam()
