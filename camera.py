from enum import Enum
import numpy as np
import cv2
from time import time

class CameraRecordState(Enum):
    NOT_RECORDING = 0
    MANUAL = 1
    AUTOMATIC = 2

class Camera:
    def __init__(self):
        self.capturing_video = CameraRecordState.NOT_RECORDING
    
    def capture_frame(self, transformed = True):
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
        self.capturing_video = state
        return True

    def stop_video_capture(self):
        if self.capturing_video == CameraRecordState.NOT_RECORDING:
            return False

        # TODO stop capturing video
        video_buffer = self.stop_recording()
        self.capturing_video = CameraRecordState.NOT_RECORDING
        return video_buffer
    
    def is_recording(self):
        return self.capturing_video != CameraRecordState.NOT_RECORDING

class DebugCamera(Camera):
    colors = [
        [0, 0, 255],
        [0, 127, 255],
        [0, 255, 255],
        [0, 255, 0],
        [255, 0, 0],
        [130, 0, 75],
        [211, 0, 148]
    ]

    cycle_time = 30

    def lerp(a, b, t):
        return (1.0 - t) * a + b * t
    
    def color_lerp(color_a, color_b, t):
        color_a_b = float(color_a[2]) / 255.0
        color_a_g = float(color_a[1]) / 255.0
        color_a_r = float(color_a[0]) / 255.0

        color_b_b = float(color_b[2]) / 255.0
        color_b_g = float(color_b[1]) / 255.0
        color_b_r = float(color_b[0]) / 255.0

        return [int(DebugCamera.lerp(color_a_b, color_b_b, t) * 255.0), int(DebugCamera.lerp(color_a_g, color_b_g, t) * 255.0), int(DebugCamera.lerp(color_a_r, color_b_r, t) * 255.0)]
    
    def get_current_color(self):
        current_color_index = int(((time() % self.cycle_time) / self.cycle_time) * len(self.colors))
        current_color = self.colors[current_color_index]
        next_color = self.colors[(current_color_index + 1) % len(self.colors)]

        return DebugCamera.color_lerp(current_color, next_color, (time() % (self.cycle_time / len(self.colors))) / (self.cycle_time / len(self.colors)))

    def capture_frame(self, transformed):
        current_color = self.get_current_color()
        return cv2.imencode('.jpeg', (np.zeros([480,720,3],dtype=np.uint8) + current_color))[1].tobytes()
    
    def start_recording(self):
        pass

    def stop_recording(self):
        return None