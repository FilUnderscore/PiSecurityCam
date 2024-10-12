from picamera2 import Picamera2
from io import BytesIO, BufferedIOBase
from datetime import datetime
from picamera2.encoders import MJPEGEncoder, H264Encoder
from picamera2.outputs import FileOutput, CircularOutput
from threading import Condition
import subprocess
import os
import cv2
import numpy as np
from enum import Enum
from senseHatLED import SenseHatLED 

encoder = H264Encoder()
output = CircularOutput(buffersize=30*3)

def h264_to_mp4(file_path, output_file_path):
    try:
        command = ['ffmpeg', '-y', '-i', file_path, '-c', 'copy', output_file_path]
        subprocess.run(command, check=True)
        return True
    except subprocess.CalledProcessError:
        print('Error occurred when converting h264 to mp4.')
        return False

class CameraRecordState(Enum):
    NOT_RECORDING = 0
    MANUAL = 1
    AUTOMATIC = 2

class Camera:
    def __init__(self):
        self.capturing_video = CameraRecordState.NOT_RECORDING
        self.led = SenseHatLED()  # Initialize the SenseHatLED instance
    
    def capture_frame(self):
        pass

    def capture_picture(self):
        frame = self.capture_frame(False)
        return frame

    def start_recording(self):
        pass

    def stop_recording(self):
        pass
    
    def start_video_capture(self, state):
        if self.capturing_video != CameraRecordState.NOT_RECORDING:
            return False
        
        # TODO capture video
        self.start_recording()
        if state == CameraRecordState.MANUAL:
            print("Manual Recording Started")
        else:
            self.led.set_red()  # Red LED for automatic motion-based recording
        self.capturing_video = state
        return True

    def stop_video_capture(self):
        if self.capturing_video == CameraRecordState.NOT_RECORDING:
            return False

        # TODO stop capturing video
        video_buffer = self.stop_recording()
        self.capturing_video = CameraRecordState.NOT_RECORDING
        self.led.set_green()  # Set LED to green after stopping recording
        return video_buffer
    
    def is_recording(self):
        return self.capturing_video != CameraRecordState.NOT_RECORDING

class StreamingOutput(BufferedIOBase):
    def __init__(self, transform):
        self.frame = None
        self.transform = transform
        self.condition = Condition()
    
    def write(self, buf):
        with self.condition:
            self.frame = buf

            if self.transform != None:
                self.transformed_frame = self.transform(buf)
            
            self.condition.notify_all()

class PiCamera(Camera):
    def __init__(self, transform = None):
        Camera.__init__(self)
        self.picam2 = Picamera2()

        camera_config = self.picam2.create_video_configuration(main={"size": (720, 480)})
        self.picam2.configure(camera_config)
        self.picam2.set_controls({"FrameRate": 15})

        self.encoder = MJPEGEncoder(10000000)
        self.streamOut = StreamingOutput(transform)
        self.streamOut2 = FileOutput(self.streamOut)
        self.encoder.output = [self.streamOut2]
        self.picam2.start_encoder(self.encoder)
        self.picam2.start_recording(encoder, output)
        self.picam2.start()

        self.led.set_green()  # Set LED to green when the camera is turned on

    def capture_frame(self, transformed = True):        
        with self.streamOut.condition:
            self.streamOut.condition.wait()

            if transformed == False:
                frame_data = self.streamOut.frame
            else:
                frame_data = self.streamOut.transformed_frame

        return frame_data

    def start_recording(self):
        output.fileoutput = 'test_vid.h264'
        output.start()
        print('Start')

    def stop_recording(self):
        output.stop()
        
        if h264_to_mp4('test_vid.h264', 'test_vid.mp4'):
            print('Stop')
            
            with open('test_vid.mp4', 'rb') as f:
                buffer = BytesIO(f.read())
            
            os.remove('test_vid.h264')
            os.remove('test_vid.mp4')

            return buffer
        else:
            return None

class DebugCamera(Camera):
    def __init__(self):
        pass

    def capture_frame(self):
        pass

class MotionPiCamera(PiCamera):
    first_frame = None
    motion_detected = False

    def __init__(self, database):
        PiCamera.__init__(self, self.transform_frame)
        self.database = database

    def detect_motion(self, frame, gray_frame, first_frame, min_area=1000):
        # Compute the absolute difference between the current frame and the first frame

        frame_delta = cv2.absdiff(first_frame, gray_frame)

        thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]

        thresh = cv2.dilate(thresh, None, iterations=2)

        # Find contours of the thresholded image

        contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        valid_contour = False

        for contour in contours:

            if cv2.contourArea(contour) < min_area:
                continue

            # Get the bounding box coordinates for the contour

            (x, y, w, h) = cv2.boundingRect(contour)

            # Draw a rectangle around the moving object

            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            valid_contour = True
        
        self.motion_detected = valid_contour
        return frame
    
    def transform_frame(self, captured_frame):
        frame = cv2.imdecode(np.frombuffer(captured_frame, np.uint8), -1)

        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        if self.first_frame is None:
            self.first_frame = gray
            return cv2.imencode('.jpg', frame)[1].tobytes()
        
        frame_with_motion = self.detect_motion(frame, gray, self.first_frame)
        
        if self.capturing_video == CameraRecordState.NOT_RECORDING and self.motion_detected == True:
            self.start_video_capture(CameraRecordState.AUTOMATIC)
            print('Start - we got motion')
        elif self.capturing_video == CameraRecordState.AUTOMATIC and self.motion_detected == False:
            video_buffer = self.stop_video_capture()

            if video_buffer != None:
                self.database.insert("videos", {"timestamp": datetime.strftime(datetime.now(), '%d-%m-%Y %H:%M:%S'), "video": video_buffer.read().hex(), "motion": "true"})
            
            print('Stop - no more motion')

        return cv2.imencode('.jpg', frame_with_motion)[1].tobytes()
    
    def reset_first_frame(self):
        self.first_frame = None
