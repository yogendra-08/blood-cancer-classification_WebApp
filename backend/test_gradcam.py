import os
import numpy as np
import cv2
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.efficientnet import preprocess_input
from tensorflow.keras.models import load_model
import tensorflow as tf

# Load the model
model = load_model('model/best_efficientnet.keras', compile=False)

# Find an uploaded image to test with
uploads_dir = 'uploads'
test_image = None
if os.path.exists(uploads_dir):
    for filename in os.listdir(uploads_dir):
        if filename.endswith(('.jpg', '.jpeg', '.png')):
            test_image = os.path.join(uploads_dir, filename)
            break

if test_image is None:
    print("No test image found in uploads directory")
    exit()

print(f"Testing with image: {test_image}")

def generate_gradcam(img_path, class_index):
    """Generate GradCAM heatmap for model interpretation"""
    try:
        print(f"Generating GradCAM for class {class_index}")
        
        # Load and preprocess image
        img = image.load_img(img_path, target_size=(224, 224))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)
        
        # Find the last convolutional layer
        last_conv_layer = None
        for layer in reversed(model.layers):
            if 'conv' in layer.name.lower():
                last_conv_layer = layer.name
                break
        
        if last_conv_layer is None:
            print("No convolutional layer found")
            return None
        
        print(f"Using layer: {last_conv_layer}")
        
        # Create a model that maps the input image to the activations
        # of the last conv layer as well as the output predictions
        grad_model = tf.keras.models.Model(
            [model.input], 
            [model.get_layer(last_conv_layer).output, model.output]
        )
        
        # Compute the gradient of the top predicted class for
        # an output feature map of the last conv layer
        with tf.GradientTape() as tape:
            # Get the model outputs
            conv_outputs, predictions = grad_model(img_array)
            # Handle case where predictions might be a list
            if isinstance(predictions, list):
                predictions = predictions[0]
            # Watch the convolutional layer output
            tape.watch(conv_outputs)
            loss = predictions[:, class_index]
        
        # Get gradients of the predicted class with respect to the output feature map
        grads = tape.gradient(loss, conv_outputs)
        
        print(f"Gradients shape: {grads.shape if grads is not None else 'None'}")
        print(f"Conv outputs shape: {conv_outputs.shape}")
        
        if grads is None:
            print("Gradients are None")
            return None
        
        # Pool the gradients across all spatial axes
        pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
        
        # Get the activations of the last conv layer
        last_conv_layer_output = conv_outputs[0]
        
        # Weight the gradients by the pooled gradients
        heatmap = tf.multiply(last_conv_layer_output, pooled_grads)
        heatmap = tf.reduce_mean(heatmap, axis=-1)
        heatmap = tf.squeeze(heatmap)
        
        # For visualization purpose, we will also normalize heatmap
        heatmap = tf.maximum(heatmap, 0) / (tf.math.reduce_max(heatmap) + 1e-8)
        heatmap = heatmap.numpy()
        
        print(f"Heatmap shape: {heatmap.shape}")
        
        # Load original image
        original_img = cv2.imread(img_path)
        if original_img is None:
            print(f"Failed to load image: {img_path}")
            return None
            
        original_img = cv2.resize(original_img, (224, 224))
        
        # Resize heatmap to match original image size
        heatmap = cv2.resize(heatmap, (original_img.shape[1], original_img.shape[0]))
        heatmap = np.uint8(255 * heatmap)
        
        # Apply colormap to heatmap
        heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
        
        # Superimpose heatmap on original image
        superimposed_img = cv2.addWeighted(original_img, 0.6, heatmap, 0.4, 0)
        
        print("GradCAM generated successfully")
        return superimposed_img
    except Exception as e:
        print(f"Error generating GradCAM: {e}")
        import traceback
        traceback.print_exc()
        return None

# Test prediction first
img_array = preprocess_image = image.load_img(test_image, target_size=(224, 224))
img_array = image.img_to_array(img_array)
img_array = np.expand_dims(img_array, axis=0)
img_array = preprocess_input(img_array)

predictions = model.predict(img_array)
predicted_class_index = np.argmax(predictions[0])
print(f"Predicted class index: {predicted_class_index}")

# Test GradCAM generation
gradcam_result = generate_gradcam(test_image, predicted_class_index)

if gradcam_result is not None:
    # Save the result
    output_path = 'test_gradcam.jpg'
    cv2.imwrite(output_path, gradcam_result)
    print(f"GradCAM test successful! Saved to: {output_path}")
else:
    print("GradCAM test failed!")
