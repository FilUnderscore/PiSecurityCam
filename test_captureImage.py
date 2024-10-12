# Using picamera to capture an image

from picamera2 import Picamera2

cam = Picamera2()
cam.start_and_capture_file("test_image.jpg")
cam.close()
