import cv2
import numpy as np
from hardware.camera.camera_constants import *
from core.installation_constants import *


class CameraManager:
    def __init__(self):
        self.cam = None #No camera open yet

    
    def start(self):

        if DEV_MODE:
            print("DEV_MODE: Camera Not Started")
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
            
        print("Cam Runnning")

    def capture(self):


        if DEV_MODE:
            print("DEV_MODE: Camera Not Started")
            return
        
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


    def preview_frame(self):
        if self.cam is not None:
            return self.cam.capture_array()
        return None

    def stop(self):
        if self.cam is not None:
           # self.cam.release() #tells cv2 to close the connection to the camera hardware
            self.cam.stop()
            self.cam = None