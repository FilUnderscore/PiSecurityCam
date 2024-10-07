"""
Model: HOG
Input: Live camera
Requirements: HOG from cv2 library

Status: works on laptop, poor accuracy
"""

import cv2
import time

# Use hog and local computer camera

# Initialize HOG descriptor for people detection
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

# Initialize webcam (0 is the default camera index for your laptop)
cap = cv2.VideoCapture(0)

# Check if the webcam is opened correctly
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

while True:
    # Capture frame from webcam
    ret, frame = cap.read()

    if ret:
        start_time = time.time()

        # Resize frame to improve frame rate (optional)
        frame = cv2.resize(frame, (1280, 720))

        # Convert frame to grayscale for HOG detector
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

        # Perform pedestrian detection
        # Perform pedestrian detection
        rects, weights = hog.detectMultiScale(
            gray_frame, 
            winStride=(4, 4), 
            padding=(8, 8), 
            scale=1.05,  # Lower the scale to handle bigger objects
        )

        # Measure elapsed time for detections
        end_time = time.time()
        print("Elapsed time:", end_time - start_time)

        # Draw bounding boxes for detected pedestrians
        for i, (x, y, w, h) in enumerate(rects):
            if weights[i] < 0.7:
                continue
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Display the frame with detected pedestrians
        cv2.imshow("Webcam - Human Detection", frame)

    # Exit condition
    k = cv2.waitKey(1)
    if k & 0xFF == ord("q"):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()