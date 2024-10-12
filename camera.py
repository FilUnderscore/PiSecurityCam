from picamera2 import Picamera2
from io import BytesIO, BufferedIOBase
from datetime import datetime
from picamera2.encoders import MJPEGEncoder, H264Encoder
from picamera2.outputs import FileOutput, CircularOutput
from threading import Condition
import subprocess
import os

encoder = H264Encoder()
output = CircularOutput(buffersize=30*3)

def h264_to_mp4(file_path, output_file_path):
    command = ['ffmpeg', '-y', '-i', file_path, '-c', 'copy', output_file_path]
    subprocess.run(command, check=True)

class Camera:
    def __init__(self):
        self.capturing_video = False
    
    def capture_frame(self):
        pass

    def capture_picture(self):
        frame = self.capture_frame()
        return frame

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
        video_buffer = self.stop_recording()
        self.capturing_video = False
        return video_buffer

class StreamingOutput(BufferedIOBase):
    def __init__(self):
        self.frame = None
        self.condition = Condition()
    
    def write(self, buf):
        with self.condition:
            self.frame = buf
            self.condition.notify_all()

class PiCamera(Camera):
    def __init__(self):
        Camera.__init__(self)
        self.picam2 = Picamera2()

        camera_config = self.picam2.create_video_configuration(main={"size": (720, 480)})
        self.picam2.configure(camera_config)
        self.picam2.set_controls({"FrameRate": 15})

        self.encoder = MJPEGEncoder(10000000)
        self.streamOut = StreamingOutput()
        self.streamOut2 = FileOutput(self.streamOut)
        self.encoder.output = [self.streamOut2]
        self.picam2.start_encoder(self.encoder)
        self.picam2.start_recording(encoder, output)
        self.picam2.start()

    def capture_frame(self):        
        with self.streamOut.condition:
            self.streamOut.condition.wait()
            frame_data = self.streamOut.frame

        return frame_data

    def start_recording(self):
        output.fileoutput = 'test_vid.h264'
        output.start()
        print('Start')

    def stop_recording(self):
        output.stop()
        h264_to_mp4('test_vid.h264', 'test_vid.mp4')
        print('Stop')
        
        with open('test_vid.mp4', 'rb') as f:
            buffer = BytesIO(f.read())
        
        os.remove('test_vid.h264')
        os.remove('test_vid.mp4')

        return buffer

class DebugCamera(Camera):
    def __init__(self):
        pass

    def capture_frame(self):
        pass
