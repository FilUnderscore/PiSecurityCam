from flask import Flask, render_template, Response, request, redirect
from camera import PiCamera
from db.sqlite_database import SqliteDatabase
from base64 import b64encode
from datetime import datetime

app = Flask(__name__)
database = SqliteDatabase("test.db")
camera = PiCamera()
video_capture = False

@app.route("/", methods=['GET', 'POST'])
def main():
        global video_capture
        form_response = None
        
        if request.method == 'POST':
                if request.form.get('capture_picture') == 'Capture Picture':
                        picture_data = camera.capture_picture()
                        database.insert("photos", {"timestamp": datetime.strftime(datetime.now(), '%d-%m-%Y %H:%M:%S'), "picture": picture_data.hex()})
                        form_response = "Success, screenshot was saved to the database."
                        print('Success')
                elif request.form.get('start_capture_video') == 'Start capturing video':
                        camera.start_video_capture()
                        video_capture = True
                        form_response = "Started recording."
                        print('Capture')
                elif request.form.get('stop_capture_video') == 'Stop capturing video':
                        video_buffer = camera.stop_video_capture()
                        database.insert("videos", {"timestamp": datetime.strftime(datetime.now(), '%d-%m-%Y %H:%M:%S'), "video": video_buffer.read().hex()})
                        video_capture = False
                        form_response = "Stopped recording."
                        print('Stop capture')
                elif request.form.get('view_motion_history') == 'View Motion History':
                        return redirect('/motion')
                elif request.form.get('view_capture_history') == 'View captures':
                        return redirect('/db')
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

@app.route("/motion")
def motion():
        pass

@app.route("/db", methods=['GET', 'POST'])
def db_view():
        if request.method == 'POST':
                if request.form.get('live_feed') == 'Back to live feed':
                        return redirect('/')
                if request.form.get('view_photos') == 'View captured photos':
                        picture_data = database.list("photos")
                        photos = []

                        for picture in picture_data:
                                picture_hex = picture['picture']
                                picture_b64 = b64encode(bytes.fromhex(picture_hex)).decode()
                                picture_timestamp = picture['timestamp']
                                photo = {"timestamp": picture_timestamp, "image_data": picture_b64}
                                photos.append(photo)

                        return render_template('db.html', photos=photos)
                elif request.form.get('view_videos') == 'View captured videos':
                        video_data = database.list('videos')
                        videos = []

                        for video in video_data:
                                video_hex = video['video']
                                video_b64 = b64encode(bytes.fromhex(video_hex)).decode()
                                video_timestamp = video['timestamp']
                                video = {"timestamp": video_timestamp, "video_data": video_b64}
                                videos.append(video)
                        
                        return render_template('db.html', videos=videos)
        
        return render_template('db.html')

app.run()
