from flask import Flask, render_template, Response, request, redirect
from base64 import b64encode

webserver_instance = None

class Webserver:
        def __init__(self, app):
                self.app = app

                global webserver_instance

                if webserver_instance != None:
                        print('Webserver has already been initialized!')
                        return

                webserver_instance = self
                flask_app.run()

flask_app = Flask(__name__)
video_capture = False

@flask_app.route("/", methods=['GET', 'POST'])
def main():
        global video_capture
        form_response = None
        
        if request.method == 'POST':
                if request.form.get('capture_picture') == 'Capture Picture':
                        if webserver_instance.app.capture_picture():
                                form_response = "Success, screenshot was saved to the database."
                        else:
                                form_response = "Failed to save screenshot to the database."
                elif request.form.get('start_capture_video') == 'Start capturing video':
                        if webserver_instance.app.start_video_capture():
                                video_capture = True
                                form_response = "Started recording."
                        else:
                                form_response = "Failed to start recording."
                elif request.form.get('stop_capture_video') == 'Stop capturing video':
                        if webserver_instance.app.stop_video_capture():
                                form_response = "Success, recording was saved to the database."
                                video_capture = False
                        else:
                                form_response = "Failed to save recording to the database."
                elif request.form.get('view_capture_history') == 'View captures':
                        return redirect('/db')
                elif request.form.get('recalibrate_motion') == 'Recalibrate motion detector':
                        try:
                                webserver_instance.app.recalibrate_motion_detector()
                                form_response = "Recalibrated motion detector."
                        except AttributeError:
                                form_response = "This camera does not support motion detection."
        
        return render_template('index.html', form_response=form_response, video_capture=video_capture)

def get_camera_feed():
	# get camera feed
        while True:
                frame = webserver_instance.app.capture_frame()
                yield (b'--frame\r\n' + b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@flask_app.route("/video_feed")
def video_feed():
	return Response(get_camera_feed(), mimetype='multipart/x-mixed-replace; boundary=frame')

@flask_app.route("/db", methods=['GET', 'POST'])
def db_view():
        if request.method == 'POST':
                if request.form.get('live_feed') == 'Back to live feed':
                        return redirect('/')
                if request.form.get('view_photos') == 'View captured photos':
                        picture_data = webserver_instance.app.get_captured_photos()
                        photos = []

                        for picture in picture_data:
                                picture_hex = picture['picture']
                                picture_b64 = b64encode(bytes.fromhex(picture_hex)).decode()
                                picture_timestamp = picture['timestamp']
                                photo = {"timestamp": picture_timestamp, "image_data": picture_b64}
                                photos.append(photo)

                        return render_template('db.html', photos=photos)
                elif request.form.get('view_videos') == 'View captured videos':
                        video_data = webserver_instance.app.get_captured_videos(request.form.get('motion'))
                        videos = []

                        for video in video_data:
                                video_hex = video['video']
                                video_b64 = b64encode(bytes.fromhex(video_hex)).decode()
                                video_timestamp = video['timestamp']
                                video = {"timestamp": video_timestamp, "video_data": video_b64}
                                videos.append(video)
                        
                        return render_template('db.html', videos=videos)
        
        return render_template('db.html')