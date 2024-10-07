"""
Model: HOG
Input: Live camera
Requirements: HOG from cv2 library

Status: works on laptop, poor accuracy, compatible with raspi
"""

from picamera2 import Picamera2
import cv2
import time

# Use hog and raspi camera

# Initialize HOG descriptor for people detection
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

# Initialize pi camera code
picam2 = Picamera2()
picam2.configure(picam2.create_still_configuration(main={"size": (720, 360)}))
picam2.start()


while True:
    # Capture frame from pi camera device
    frame = picam2.capture_array()

    if frame is not None:
        start_time = time.time()
        
        # Convert frame to grayscale for HOG compatibility
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        
        # Use model to detect people
        rects, weights = hog.detectMultiScale(
           gray_frame,
           winStride=(4,4),
           padding=(8,8),
           scale=1.01           
        )
        
        # Measure time for detections
        end_time = time.time()
        print("Elapsed time:", end_time - start_time)
        
        # Display rectangles
        for i, (x, y, w, h) in enumerate(rects):
            if weights[i] < 0.7:
                continue
            cv2.rectangle(frame, (x,y), (x + w, y + h), (0, 255, 0), 2)
            
            # Display frame
            cv2.imshow("Human Detection", frame)

    # Exit condition
    k = cv2.waitKey(1)
    if k & 0xFF == ord("q"):
        break

# Cleanup
picam2.stop()
cv2.destroyAllWindows()