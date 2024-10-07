from flask import Flask, render_template, Response, jsonify, send_file
from camera import PiCamera
import time
from io import BytesIO

app = Flask(__name__)
camera = PiCamera()

@app.route("/")
def main():
	return "Test"

@app.route("/test")
def get_camera_feed():
	# get camera feed
        while True:
                frame = camera.capture_frame()
                yield (b'--frame\r\n' + b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route("/video_feed")
def video_feed():
	return Response(get_camera_feed(), mimetype='multipart/x-mixed-replace; boundary=frame')

app.run()
