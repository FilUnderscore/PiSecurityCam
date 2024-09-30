# Import necessary packages
import numpy as np
import cv2
from picamera2 import Picamera2

# Initialize the HOG descriptor/person detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

# If using the Raspberry Pi camera module, use this command:
# For Pi Camera
#cap = cv2.VideoCapture(0, cv2.CAP_V4L2)

camera = Picamera2()

# Configure the camera with the settings provided
config = camera.create_still_configuration(
    main={"size": (4056, 3040)},
    lores={"size": (320, 240)},
    display="lores",
    buffer_count=3,
    queue=False
)
camera.configure(config)

# If using a USB webcam, you can leave it as:
# cap = cv2.VideoCapture(0)

# Set the camera resolution (reduce it to help with performance)
#cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
#cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

# Create VideoWriter object to save the output video
#out = cv2.VideoWriter(
#   'output.avi',
#   cv2.VideoWriter_fourcc(*'MJPG'),
#   15.,  # FPS
#   (320, 240))  # Frame size

camera.set_controls({"ExposureTime": 10000, "AnalogueGain": 5})
camera.start()

while True:
    frame = camera.capture_array()
    
    # Resize the frame for faster detection
    frame_resized = cv2.resize(frame, (320, 240))

    # Convert to grayscale for faster processing
    gray = cv2.cvtColor(frame_resized, cv2.COLOR_RGB2GRAY)

    # Detect people in the image
    boxes, weights = hog.detectMultiScale(frame_resized, winStride=(8, 8))

    print("Raw boxes: " + str(len(boxes)) + " raw weights: " + str(len(weights)))

    # Convert bounding boxes into the correct format
    boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])

    print("Boxes: " + str(len(boxes)))

    # Draw rectangles around detected people
    for (xA, yA, xB, yB) in boxes:
        cv2.rectangle(frame_resized, (xA, yA), (xB, yB), (0, 255, 0), 2)

    # Write the output video
    #out.write(frame_resized)

    # Display the resulting frame
    cv2.imshow('Frame', frame_resized)
    
    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and video writer
#cap.release()
#out.release()

# Destroy all OpenCV windows
cv2.destroyAllWindows()