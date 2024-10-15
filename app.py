from datetime import datetime
from camera import CameraRecordState

class App:
    def __init__(self, camera, database):
        self.camera = camera
        self.database = database
    
    def capture_picture(self):
        picture_data = self.camera.capture_picture()

        if picture_data == None:
            return False
        
        self.database.insert("photos", {"timestamp": datetime.strftime(datetime.now(), '%d-%m-%Y %H:%M:%S'), "picture": picture_data.hex()})
        return True
    
    def start_video_capture(self):
        self.camera.start_video_capture(CameraRecordState.MANUAL)
        return True
    
    def stop_video_capture(self):
        video_buffer = self.camera.stop_video_capture()

        if video_buffer == None:
            return False
        
        self.database.insert("videos", {"timestamp": datetime.strftime(datetime.now(), '%d-%m-%Y %H:%M:%S'), "video": video_buffer.read().hex(), "motion": "false"})
        return True
    
    def recalibrate_motion_detector(self):
        self.camera.recalibrate_motion_detector()
    
    def capture_frame(self):
        return self.camera.capture_frame(True)
    
    def get_captured_photos(self):
        return self.database.list('photos')
    
    def get_captured_videos(self, motion):
        if motion:
            return self.database.select('videos', [], 'motion = \'true\'')
        else:
            return self.database.list('videos')