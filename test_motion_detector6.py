"""
Status:
Title: Human walking motion detection
Author: Daniel
Description: Use HOG model stored in xml file to draw boxes on the moving object
             the moving object is currently limited to pedestrian walking
             currently will need a sample test video, place in the same directory
             and also the model as xml, place in the same directory
             Input: live camera from raspi
"""

import cv2
import time
from picamera2 import Picamera2

# Initialize HOG descriptor for people detection
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

# Initialize the Picamera2
picam2 = Picamera2()

# Configure the camera to the desired resolution
camera_config = picam2.create_preview_configuration(main={"size": (1280, 720)})
picam2.configure(camera_config)
picam2.start()

while True:
    # Capture frame from the camera
    frame = picam2.capture_array()

    if frame is not None:
        start_time = time.time()

        # Convert frame to grayscale for HOG detector
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

        # Perform pedestrian detection
        rects, weights = hog.detectMultiScale(gray_frame)

        # Measure elapsed time for detections
        end_time = time.time()
        print("Elapsed time:", end_time - start_time)

        # Draw bounding boxes for detected pedestrians
        for i, (x, y, w, h) in enumerate(rects):
            if weights[i] < 0.7:
                continue
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Display the frame with detected pedestrians
        cv2.imshow("PiCamera2 - Human Detection", frame)

    # Exit condition
    k = cv2.waitKey(1)
    if k & 0xFF == ord("q"):
        break

# Cleanup
cv2.destroyAllWindows()
picam2.close()