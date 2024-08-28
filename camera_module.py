import cv2

# Initialize video capture
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Camera could not be opened.")
    exit()

fgbg = cv2.createBackgroundSubtractorMOG2()

while True:
    ret, frame = cap.read()
    
    if not ret or frame is None:
        print("Error: Failed to capture image or frame is None.")
        break

    if frame.shape[0] == 0 or frame.shape[1] == 0:
        print("Error: Frame size is zero.")
        continue

    fgmask = fgbg.apply(frame)
    
    th = cv2.threshold(fgmask, 200, 255, cv2.THRESH_BINARY)[1]
    
    contours, _ = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    print(f"Number of contours detected: {len(contours)}")

    for contour in contours:
        area = cv2.contourArea(contour)
        
        if area > 100:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    
    cv2.imshow('frame', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
