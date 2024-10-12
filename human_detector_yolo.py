# Model: YOLOv3 tiny
# Req: weights, config .cfg, class coco.names

import cv2
import time
from picamera2 import Picamera2

# Load YOLO model
net = cv2.dnn.readNet("yolov3-tiny.weights", "yolov3-tiny.cfg")
layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

# Load COCO class labels
with open("coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]

# Initialize Picamera2
picam2 = Picamera2()
config = picam2.create_still_configuration(main={"size": (720, 360)})
picam2.configure(config)
picam2.start()

while True:
    # Capture frame from PiCamera2
    frame = picam2.capture_array()

    # Convert frame to BGR for DNN input
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    # Prepare the frame for YOLO
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)

    # Perform detection
    outs = net.forward(output_layers)

    # Initialize lists for detection results
    class_ids = []
    confidences = []
    boxes = []

    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            if confidence > 0.5 and classes[class_id] == "person":  # Only detect persons
                center_x = int(detection[0] * frame.shape[1])
                center_y = int(detection[1] * frame.shape[0])
                w = int(detection[2] * frame.shape[1])
                h = int(detection[3] * frame.shape[0])

                # Calculate coordinates for bounding box
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    # Apply Non-Maximum Suppression to eliminate multiple detections
    indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    for i in indices:
        i = i[0]
        x, y, w, h = boxes[i]
        label = str(classes[class_ids[i]])
        confidence = confidences[i]

        # Draw bounding box
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, f"{label} {confidence:.2f}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # Display the frame
    cv2.imshow("PiCamera - Human Detection", frame)

    # Exit condition
    k = cv2.waitKey(1)
    if k & 0xFF == ord("q"):
        break

# Cleanup
cv2.destroyAllWindows()