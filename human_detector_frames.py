import cv2
import numpy as np
from picamera2 import Picamera2
import time

# Initialize the PiCamera2
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": "RGB888"}))
picam2.start()

time.sleep(2)  # Let the camera warm up

# Initialize variables for motion detection
first_frame = None
motion_detected = False

# Define a function to detect motion
def detect_motion(frame, gray_frame, first_frame, min_area=500):
    global motion_detected

    # Compute the absolute difference between the current frame and the first frame
    frame_delta = cv2.absdiff(first_frame, gray_frame)
    thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2)

    # Find contours of the thresholded image
    contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    motion_detected = False

    for contour in contours:
        if cv2.contourArea(contour) < min_area:
            continue

        # Motion detected
        motion_detected = True

        # Get the bounding box coordinates for the contour
        (x, y, w, h) = cv2.boundingRect(contour)

        # Draw a rectangle around the moving object
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    return frame

while True:
    # Capture a frame from the camera
    frame = picam2.capture_array()

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

    # Blur the frame to reduce noise and improve motion detection accuracy
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    # If this is the first frame, use it as the background model for motion detection
    if first_frame is None:
        first_frame = gray
        continue

    # Detect motion and draw the bounding box if motion is detected
    frame_with_motion = detect_motion(frame, gray, first_frame)

    # Display the frame with motion boxes
    cv2.imshow("Motion Detection", frame_with_motion)

    # Exit when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cv2.destroyAllWindows()
picam2.stop()