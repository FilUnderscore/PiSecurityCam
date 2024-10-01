"""
Title: Human walking motion detection
Author: Daniel
Description: Use haarcascade full body model stored in xml file to draw boxes on the moving object
             The moving object is currently limited to pedestrian walking.
             Requires a sample test video or direct camera input via Raspberry Pi Camera Module 2.
"""

import cv2
import time
import os
from picamera2 import Picamera2
import numpy as np

# Load the pre-trained Haar Cascade model for full body detection
person_cascade = cv2.CascadeClassifier(os.path.join('haarcascade_fullbody.xml'))

# Initialize the Picamera2 object
picam2 = Picamera2()
config = picam2.create_preview_configuration(main={"size": (640, 360)})
picam2.configure(config)
picam2.start()

while True:
    # Capture a frame from the Raspberry Pi Camera Module
    frame = picam2.capture_array()
    
    # Fix RGB to BGR to follow OpenCV display
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    # Start time to measure detection performance
    start_time = time.time()

    # Convert to grayscale for Haar-cascade classifier
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

    # Detect people using Haar Cascade
    rects = person_cascade.detectMultiScale(
        gray_frame,
        scaleFactor=1.01,  # Controls the scale of the image pyramid
        minNeighbors=4
        ,    # Rejects some rectangles based on quality
        minSize=(30, 30),  # Minimum size of detected person
        maxSize=(300, 300) # Maximum size of detected person
    )
    
    # Measure elapsed time for detection
    end_time = time.time()
    print("Elapsed Time:", end_time - start_time)

    # Draw rectangles around detected persons
    for (x, y, w, h) in rects:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Display the frame with detected rectangles
    cv2.imshow("preview", frame)

    # Exit condition on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cv2.destroyAllWindows()
picam2.stop()