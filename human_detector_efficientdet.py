import numpy as np
import tflite_runtime.interpreter as tflite
from picamera2 import Picamera2
import time
import cv2 

# Load TFLite model and allocate tensors
model_path = 'efficientdet.tflite'
interpreter = tflite.Interpreter(model_path=model_path)  # Use tflite runtime
interpreter.allocate_tensors()

# Get input and output details from the interpreter
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Initialize Picamera2
camera = Picamera2()

# Configure camera capture resolution
config = camera.create_preview_configuration(main={"size": (640, 480)})
camera.configure(config)
camera.start()

def preprocess_image(frame, input_shape):
    # Resize the frame to match model input
    resized_img = cv2.resize(frame, (input_shape[1], input_shape[2]))
    # Convert the frame to UINT8 (the expected input type)
    input_data = np.array(resized_img, dtype=np.uint8)
    # Add a batch dimension
    input_data = np.expand_dims(input_data, axis=0)
    return input_data

try:
    while True:
        # Capture a frame from the PiCamera2
        frame = camera.capture_array()

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

        # Add a short delay to reduce CPU usage
        time.sleep(0.1)

finally:
    # Ensure the camera is stopped properly
    camera.stop()
    cv2.destroyAllWindows()  
