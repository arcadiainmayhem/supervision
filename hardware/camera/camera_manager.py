import cv2
import numpy as np
from hardware.camera.camera_constants import *
from core.installation_constants import *


class CameraManager:


    def __init__(self):
        self.cam = None #No camera open yet
        self.isavailable = False #initialise state

    
    def start(self):

        if DEV_MODE:
            print("DEV_MODE: Camera Not Started")
            return

        try:
            #retry and clears camera object
            if self.cam is not None: #theres something
                try:
                    self.cam.stop()
                except:
                    pass
                self.cam = None

            from picamera2 import Picamera2
            self.cam = Picamera2()
            config = self.cam.create_still_configuration(
                 main = {
                        "size" : RESOLUTION, 
                        "format" : "BGR888"
                })
            self.cam.configure(config)
            self.cam.start()

            #controls
            self.cam.set_controls({
                    "AwBEnable" : True, #auto white balance
                    "AeEnable"  : True, #Auto Exposure
            })

            self.isavailable = True #flip flag because cam is available

            print("Cam Runnning")

        except Exception as e:
            self.cam = None
            self.isavailable = False
            print(f"Camera Failed to Start: {e}")


    def capture(self):

        if DEV_MODE:
            print("DEV_MODE: Camera Not Started")
            return
        
        if not self.isavailable:
            print("[CAMERA MANAGER] Unavailable - Attempting Restart")
            self.start()

        try:
            if self.cam is not None and self.isavailable:
                frame = self.cam.capture_array()
                return frame
            return None
        

        except Exception as e:
            self.isavailable = False
            print(f"[CAMERAMANGER] Capture Failed: {e}")
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
            frame = self.cam.capture_array()
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            return frame
        return None

    def stop(self):
        if self.cam is not None:
           # self.cam.release() #tells cv2 to close the connection to the camera hardware
            self.cam.stop()
            self.cam = None