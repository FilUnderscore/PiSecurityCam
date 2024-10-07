from picamera2 import Picamera2
from io import BytesIO
from datetime import datetime

class Camera:
    def __init__(self):
        self.capturing_video = False
    
    def capture_frame(self):
        pass

    def capture_picture(self):
        frame = self.capture_frame()
        filename = datetime.now().strftime('%d-%m-%y_%H_%M_%S.jpg')

        with open(filename, 'wb') as f:
            f.write(frame)

        print('Saved as ' + filename)
        return filename

    def start_video_capture(self):
        if self.capturing_video == True:
            return False
        
        # TODO capture video
        return True

    def stop_video_capture(self):
        if self.capturing_video == False:
            return False

        # TODO stop capturing video
        return True

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

class DebugCamera(Camera):
    def __init__(self):
        pass

    def capture_frame(self):
        pass
