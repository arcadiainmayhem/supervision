import cv2
from hardware.camera.camera_constants import *


class CameraManager:
    def __init__(self):
        self.cam = None #No camera open yet

        if DEV_MODE:
            self.camera_index = DEV_CAMERA_INDEX
        else:
            self.camera_index = PI_CAMERA_INDEX

    def start(self):
        if self.cam is None:
            self.cam = cv2.VideoCapture(self.camera_index)
            print("Cam Running!")

    def capture(self):
        #read() return BGR
        if self.cam is not None:
            ret , frame = self.cam.read()
            if ret:
                return frame
        return None


    def stop(self):
        if self.cam is not None:
            self.cam.release() #tells cv2 to close the connection to the camera hardware
            self.cam = None