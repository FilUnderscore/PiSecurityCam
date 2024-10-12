import cv2
import numpy as np
import time
import datetime

# Initialize the webcam (0 is the default camera)
cap = cv2.VideoCapture(1)

# Let the camera warm up
time.sleep(2)

# Initialize variables for motion detection and video recording
first_frame = None
motion_detected = False
recording = False
video_writer = None
no_motion_counter = 0  # Used to wait before stopping the recording when motion stops

# Define a function to detect motion
def detect_motion(frame, gray_frame, first_frame, min_area=5000):
    motion_detected = False

    # Compute the absolute difference between the current frame and the first frame
    frame_delta = cv2.absdiff(first_frame, gray_frame)
    thresh = cv2.threshold(frame_delta, 50, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=3)

    # Find contours
    contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour) < min_area:
            continue

        # Motion is detected if a contour with significant area is found
        motion_detected = True

        # Get the bounding box coordinates and draw a rectangle
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    return frame, motion_detected

# Start the main loop
while True:
    # Capture a frame from the webcam
    ret, frame = cap.read()

    if not ret:
        print("Failed to grab frame")
        break

    # Resize the frame (optional)
    frame = cv2.resize(frame, (640, 480))

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Blur the frame to reduce noise and improve motion detection accuracy
    gray = cv2.GaussianBlur(gray, (31, 31), 0)

    # If this is the first frame, use it as the background model for motion detection
    if first_frame is None:
        first_frame = gray
        continue

    # Detect motion and draw the bounding box if motion is detected
    frame_with_motion, motion_detected = detect_motion(frame, gray, first_frame)

    # Handle video recording
    if motion_detected:
        no_motion_counter = 0  # Reset no-motion counter when motion is detected

        if not recording:
            # Start recording video
            recording = True
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            video_filename = f"motion_{timestamp}.avi"
            fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Video codec
            video_writer = cv2.VideoWriter(video_filename, fourcc, 20.0, (640, 480))  # FPS and resolution
            print(f"Recording started: {video_filename}")

        # Write the current frame to the video
        if video_writer:
            video_writer.write(frame)

    else:
        # When no motion is detected, increment the no-motion counter
        no_motion_counter += 1

        # Stop recording if no motion is detected for a few frames (10 in this example)
        if no_motion_counter > 10 and recording:  # Delay for a few frames to avoid stopping too soon
            recording = False
            if video_writer:
                video_writer.release()
                video_writer = None
            print("Recording stopped due to no motion")

    # Display the frame
    cv2.imshow("Motion Detection", frame_with_motion)

    # Exit when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
if video_writer:
    video_writer.release()

cap.release()
cv2.destroyAllWindows()