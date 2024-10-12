"""
Model: HOG
Input: Live camera
Requirements: HOG from cv2 library

Status: works on laptop, poor accuracy, compatible with raspi
"""

import cv2
import time
from picamera2 import Picamera2

# Initialize HOG descriptor for people detection
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

# Initialize Picamera2
picam2 = Picamera2()
config = picam2.create_still_configuration(main={"size": (720, 360)})
picam2.configure(config)
picam2.start()

while True:
    # Capture frame from PiCamera2
    frame = picam2.capture_array()
    
    # Convert fram to BGR for HOG detector
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    
    # Convert frame to grayscale for HOG detector
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Perform pedestrian detection
    rects, weights = hog.detectMultiScale(
        gray_frame, 
        winStride=(4, 4), 
        padding=(8, 8), 
        scale=1.05
    )

    # Draw bounding boxes for detected pedestrians
    for i, (x, y, w, h) in enumerate(rects):
        if weights[i] < 0.7:
            continue
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Display the frame with detected pedestrians
    cv2.imshow("PiCamera - Human Detection", frame)
    cv2.imwrite('saved_image.png', frame)

    # Exit condition
    k = cv2.waitKey(1)
    if k & 0xFF == ord("q"):
        break

# Cleanup
cv2.destroyAllWindows()