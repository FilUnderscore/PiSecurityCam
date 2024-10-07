from picamera2 import Picamera2
from io import BytesIO

class Camera:
    def capture_frame(self):
        pass

class PiCamera(Camera):
    def __init__(self):
        self.picam2 = Picamera2()

        camera_config = self.picam2.create_preview_configuration(main={"size": (1280, 720)})
        self.picam2.configure(camera_config)
        self.picam2.start()

    def capture_frame(self):
        data = BytesIO()
        self.picam2.capture_file(data, format='jpeg')
        data.seek(0)
        return data.read()
        #return self.picam2.capture_array()
