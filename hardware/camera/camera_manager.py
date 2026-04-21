import cv2
import numpy as np
from hardware.camera.camera_constants import *


class CameraManager:
    def __init__(self):
        self.cam = None #No camera open yet

    
    def start(self):

        if self.cam is None:
                print("DEVMODE : No Camera Started")
                self.camera_index = DEV_CAMERA_INDEX
                return
        if self.cam is None:
            from picamera2 import Picamera2
            self.cam = Picamera2()
            config = self.cam.create_still_configuration(
                main = {
                    "size" : RESOLUTION, 
                    "format" : "BGR888"
                })
            self.cam.configure(config)
            self.cam.start()
            
        # else:
        #     self.camera_index = PI_CAMERA_INDEX

        
        # if self.cam is None:
        #     self.cam = cv2.VideoCapture(self.camera_index)
        #     print("Cam Running!")
        print("Cam Runnning")

    def capture(self):
        #read() return BGR
        # if self.cam is not None:
        #     ret , frame = self.cam.read()
        #     if ret:
        #         return frame
        # return None

        # if DEV_MODE:
        #      return cv2.imread(DEV_IMAGE_PATH)
        if self.cam is not None:
             frame = self.cam.capture_array()
             return frame
        return None

    def preview(self):
         if DEV_MODE:
              while True:
                   frame = self.cam.capture_array()
                   cv2.imshow("Preview" , frame)
                   key = cv2.waitKey(1)
                   if key == 32:
                        cv2.destroyAllWindows()
                        return frame

    def stop(self):
        if self.cam is not None:
           # self.cam.release() #tells cv2 to close the connection to the camera hardware
            self.cam.stop()
            self.cam = None