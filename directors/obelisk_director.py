import time
from hardware.button.button_listener import start
import cv2
from hardware.camera.camera_constants import *
from core.installation_constants import *
from computervision.extractor import extract_color
from computervision.classifier import classify
from computervision.imageloader import load_image
from computervision.extract_coordinates import extract_coordinates
from computervision.mediapipe.orchestrator import orchestrate_detection_pipeline
from computervision.mediapipe.detection.posedetection import setup_pose_object
from hardware.camera.camera_manager import CameraManager
from compositor.selector import select
from compositor.compose import composite_elements

#Observe

#Accumulate


#Points / Produces output

class ObeliskDirector():

    def __init__(self):
        #runs once
        self.camera = CameraManager()
        print("Camera Starting Up")
        #start camera
        self.camera.start()

        #obelisk variables
        self.isWatching = False
    
        
        self.isPrinting = False

        #current running data
        self.current_observation = None

        #initilaise mediapose object
        self.detector = setup_pose_object()
        
        

    def start_watching(self):
        self.isWatching = True
        
    def stop_watching(self):
        self.isWatching = False
        


    def _capture(self):
        if DEV_MODE:
            return load_image(DEV_IMAGE_PATH)
        else:
            print("Dev Mode", DEV_MODE)
            print("Camera Object", self.camera.cam)
            return self.camera.capture()
        
    def read_frame(self):
        #read frames for passive sampling
        pass

    def passive_continuous_observation(self, visitor):
        while self.isWatching:
            #TODO: TREADING
            #check for presence
            #check for microphone
            #update movement variance
            #update dwell time
            #write to visitor
            print("Camera is Observing")
            frame = self.camera.preview_frame()
            if frame is not None:
                cv2.imshow("Camera Preview", frame)
                cv2.waitKey(1)
            

    def observe(self,visitor):
        frame = self._capture()
        #writes to visitor dictionary
        self.run_pipeline(frame, visitor)

    def pause_observe(self, visitor):
        pass
        


    def run_pipeline(self,frame,visitor):
        
        #store in dictionary
        visitor["camera_frame"] = frame
        print("Detecting Poses...")
        detected_poses = orchestrate_detection_pipeline(frame , self.detector )
        region_crop = extract_coordinates(detected_poses , frame) # for specific region crop
        visitor["pose_detection"] = detected_poses
        #extracting color values in crop
        print("Extracting Colors..")
        color_results = extract_color(region_crop)
        visitor["color_saturation"] = color_results["average_saturation"]
        visitor["color_value"] = color_results["average_value"]
        visitor["color_hue"] = color_results["dominant_hue"]
        print("Categorising Results...")
        #classification
        categorised = classify(color_results)
        visitor["hue_category"] = categorised["hue_category"]
        visitor["brightness"] = categorised["brightness"]
        print("Selecting Elements...")
        #selected elements / pngs
        selection = select(categorised)
        visitor["selected_elements"] = selection
        
        #later for memory?

    def _return_visitor( self , visitor):
        return visitor

    def produce_selphy_card(self,visitor):
        elements = visitor["selected_elements"]
        output_image = composite_elements(elements)
        output_image.save("test/output.png")
        if DEV_MODE:
            output_image.show()
        else:
            self._print_selphy_card(output_image)
            
        return output_image

    def _print_selphy_card(self, output_image ):
        #send output image to Selphy via CUPS
        print("Connecting to Printer - Print Selphy Card")#

    def _stop_camera(self):
        self.camera.stop()

