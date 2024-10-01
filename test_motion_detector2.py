"""
Status: Working with laptop camera
Title: Human walking motion detection
Author: Daniel
Description: Efficientdet model saved as tflite
Input Type : Live camera feed from local laptop
Requirements: using LiteRT inference library and use efficientdet model saved as .tflite

NEW CODE
"""

import cv2
import numpy as np
from ai_edge_litert.interpreter import Interpreter

# Load TFLite model and allocate tensors
model_path = 'efficientdet.tflite'
interpreter = Interpreter(model_path=model_path)
interpreter.allocate_tensors()

# Get input and output details from the interpreter
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Capture video from the live webcam with specific settings
cap = cv2.VideoCapture(1, cv2.CAP_AVFOUNDATION)
cap.set(3, 640)  # Width
cap.set(4, 480)  # Height
cap.set(10, 150)  # Brightness

def preprocess_image(frame, input_shape):
    # Resize the frame to match model input
    resized_img = cv2.resize(frame, (input_shape[1], input_shape[2]))
    # Convert the frame to UINT8 (the expected input type)
    input_data = np.array(resized_img, dtype=np.uint8)
    # Add a batch dimension
    input_data = np.expand_dims(input_data, axis=0)
    return input_data

while True:
    ret, frame = cap.read()
    print(f"Frame capture success: {ret}")
    if not ret:
        print("Failed to capture image")
        break

    # Preprocess the frame to match input requirements (UINT8)
    input_data = preprocess_image(frame, input_details[0]['shape'])
    
    # Set the input tensor (UINT8 type now)
    interpreter.set_tensor(input_details[0]['index'], input_data)
    
    # Run inference
    interpreter.invoke()
    
    # Get the output tensor (bounding boxes, class IDs, and scores)
    boxes = interpreter.get_tensor(output_details[0]['index'])[0]  # Bounding box coordinates
    class_ids = interpreter.get_tensor(output_details[1]['index'])[0]  # Class IDs
    scores = interpreter.get_tensor(output_details[2]['index'])[0]  # Confidence scores

    # Apply Non-Max Suppression
    indices = cv2.dnn.NMSBoxes(boxes, scores, 0.5, 0.3)

    if len(indices) > 0:
        for i in indices.flatten():
            if class_ids[i] == 0:  # Assuming class 0 is "person"
                ymin, xmin, ymax, xmax = boxes[i]
                (imH, imW) = frame.shape[:2]
                xmin = int(xmin * imW)
                xmax = int(xmax * imW)
                ymin = int(ymin * imH)
                ymax = int(ymax * imH)
                
                # Draw a bounding box around the detected person
                cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
                cv2.putText(frame, 'Person', (xmin, ymin - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)

    # Display the frame with the bounding boxes
    cv2.imshow('Live Human Detection', frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close any OpenCV windows
cap.release()
cv2.destroyAllWindows()