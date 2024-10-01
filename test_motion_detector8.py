"""
Status: Working with laptop camera, not tested on picamera yet
Title: Human walking motion detection
Author: Daniel
Description: MobileNet SSD model for person recognition
Input Type : Live camera feed from raspberry pi
Requirements: config path file as .pbtxt and weights as .pb and class file name as coco
Yes
"""
import cv2
import numpy as np
from picamera2 import Picamera2
import time

# Set thresholds
thres = 0.45
nms_threshold = 0.2

# Initialize PiCamera2
picam2 = Picamera2()
camera_config = picam2.create_still_configuration(main={"size": (640, 480)})
picam2.configure(camera_config)
picam2.start()

# Allow camera to warm up
time.sleep(2)

# Load class names
classNames = []
classFile = 'coco.names'
with open(classFile, 'rt') as f:
    classNames = f.read().rstrip('\n').split('\n')
print(classNames)

# Load model configuration and weights
configPath = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
weightsPath = 'frozen_inference_graph.pb'

# Initialize the network model
net = cv2.dnn_DetectionModel(weightsPath, configPath)
net.setInputSize(320, 320)
net.setInputScale(1.0 / 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)

while True:
    # Capture a frame from the PiCamera2
    frame = picam2.capture_array()

    # Perform object detection
    classId, confs, bbox = net.detect(frame, confThreshold=thres)
    bbox = list(bbox)
    confs = list(np.array(confs).reshape(1, -1)[0])
    confs = list(map(float, confs))
    print(confs)

    # Apply Non-Max Suppression
    indices = cv2.dnn.NMSBoxes(bbox, confs, thres, nms_threshold)
    print(indices)

    # Ensure indices is not empty and filter for person class (class ID = 1)
    if len(indices) > 0:
        for i in indices.flatten():  # Flatten to handle both cases: 1D or 2D array
            if classId[i] == 1:  # Only detect 'person' (classId = 1 in COCO dataset)
                box = bbox[i]
                x, y, w, h = box[0], box[1], box[2], box[3]
                cv2.rectangle(frame, (x, y), (x + w, y + h), color=(0, 255, 0), thickness=2)
                
                # Fix for classId indexing, treat it as 1D array
                label = classNames[classId[i] - 1].upper()
                cv2.putText(frame, label, (x + 10, y + 30),
                            cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

    # Display the live camera feed with detections
    cv2.imshow("Live Person Detection", frame)

    # Break the loop if 'q' is pressed
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

# Release camera and close all windows
picam2.close()
cv2.destroyAllWindows()