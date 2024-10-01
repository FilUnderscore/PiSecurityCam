from flask import Flask, render_template, Response, jsonify

app = Flask(__name__)

@app.route("/")
def main():
	return "Test"

def get_camera_feed():
	# TODO get camera feed
	frame = None
	yield (b'--frame\r\n' + b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route("/video_feed")
def video_feed():
	return Response(get_camera_feed(), mimetype='multipart/x-mixed-replace; boundary=frame')

app.run()
