from flask import Flask, render_template, Response, jsonify, send_file, request
from camera import PiCamera
import time
from io import BytesIO

app = Flask(__name__)
camera = PiCamera()

@app.route("/", methods=['GET', 'POST'])
def main():
        form_response = None
        video_capture = False
        
        if request.method == 'POST':
                if request.form.get('capture_picture') == 'Capture Picture':
                        filename = camera.capture_picture()
                        form_response = "Success, screenshot was saved to " + filename + "."
                        print('Success')
                elif request.form.get('start_capture_video') == 'Start capturing video':
                        print('Capture')
                elif request.form.get('stop_capture_video') == 'Stop capturing video':
                        print('Stop capture')
        else:
                print('Request')

        return render_template('index.html', form_response=form_response, video_capture=video_capture)

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
