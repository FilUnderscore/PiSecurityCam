from picamera2 import Picamera2
from io import BytesIO
from datetime import datetime
from picamera2.encoders import H264Encoder
from picamera2.outputs import FfmpegOutput

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

    def start_recording(self):
        pass

    def stop_recording(self):
        pass
    
    def start_video_capture(self):
        if self.capturing_video == True:
            return False
        
        # TODO capture video
        self.start_recording()
        self.capturing_video = True
        return True

    def stop_video_capture(self):
        if self.capturing_video == False:
            return False

        # TODO stop capturing video
        self.stop_recording()
        self.capturing_video = False
        return True

class PiCamera(Camera):
    def __init__(self):
        Camera.__init__(self)
        self.picam2 = Picamera2()

        camera_config = self.picam2.create_video_configuration(main={"size": (1280, 720)})
        self.picam2.configure(camera_config)
        self.picam2.start()

    def capture_frame(self):
        data = BytesIO()
        self.picam2.capture_file(data, format='jpeg')
        data.seek(0)
        return data.read()
        #return self.picam2.capture_array()

    def start_recording(self):
        encoder = H264Encoder(10000000)
        self.picam2.start_recording(encoder, 'test_vid.h264')
        print('Start')

    def stop_recording(self):
        self.picam2.stop_encoder()
        print('Stop')

class DebugCamera(Camera):
    def __init__(self):
        pass

    def capture_frame(self):
        pass
