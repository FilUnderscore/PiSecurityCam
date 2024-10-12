from picamera2 import Picamera2
import cv2

# Initialize the camera
camera = Picamera2()

# Configure camera capture resolution (optional, can be adjusted)
config = camera.create_preview_configuration(main={"size": (640, 480)})
camera.configure(config)

# Start the camera
camera.start()

while True:
    # Capture a frame in RGB format
    frame = camera.capture_array()

    # Convert RGB to BGR (OpenCV uses BGR by default)
    frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    # Display the frame using OpenCV
    cv2.imshow("PiCamera2 Live Feed", frame_bgr)

    # Wait for 'q' key to be pressed to quit the loop and close the window
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Stop the camera
camera.stop()

# Close OpenCV window
cv2.destroyAllWindows()
