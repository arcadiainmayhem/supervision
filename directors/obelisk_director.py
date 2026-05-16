import time
from hardware.button.button_listener import register_trigger_button
import cv2
import threading
import subprocess
from PIL import Image
from hardware.camera.camera_constants import *
from core.installation_constants import *
from computervision.extractor import extract_color
from computervision.classifier import classify
from computervision.imageloader import load_image
from computervision.extract_coordinates import extract_coordinates


from computervision.mediapipe.orchestrator import orchestrate_detection_pipeline
from computervision.mediapipe.detection.bodydetection import setup_body_object
from computervision.mediapipe.detection.facedetection import setup_face_object
from computervision.mediapipe.detection.handdetection import setup_hand_object
from computervision.mediapipe.detection.gesture_recognizer import setup_gesture_object
from computervision.mediapipe.mediapipe_interpreter import interpret_all_mediapipe_detection

from hardware.camera.camera_manager import CameraManager
from obelisk_compositor.obelisk_card_selector import select
from obelisk_compositor.obelisk_card_compositor import composite_elements

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
    
        #printing state flag     
        self.isPrinting = False

        #theadings
        self.preview_thread = None
        self.frame_lock = threading.Lock() #like a flag - free or taken

        #current running data
        self.current_observation = None

        #initilaise mediapose objects
        self.body_detector = setup_body_object()
        self.face_detector = setup_face_object()
        self.hand_detector = setup_hand_object()
        self.gesture_recognizer = setup_gesture_object()

    def start_watching(self):
        self.isWatching = True
        self.preview_thread = threading.Thread(target=self.passive_continuous_observation)
        self.preview_thread.daemon = True
        self.preview_thread.start()

    def stop_watching(self):
        self.isWatching = False
        


    def _capture(self):
        try:
            if DEV_MODE:
                return load_image(DEV_IMAGE_PATH)
            


            else:
                print("Dev Mode", DEV_MODE)
                print("Camera Object", self.camera.cam)
                with self.frame_lock:
                    return self.camera.capture()
            
        except Exception as e:
            print(f"Camera capture failed: {e} — loading fallback image")
            return load_image(FALLBACK_IMAGE_PATH)

        
    def read_frame(self):
        #read frames for passive sampling
        pass

    def passive_continuous_observation(self):
        while self.isWatching:
            #TODO: TREADING
                with self.frame_lock: #acquire lock
                    frame = self.camera.preview_frame()
                time.sleep(0.03)
                if frame is not None:
                    #print("Camera is Observing")
                    cv2.imshow("Camera Preview", frame)
                    cv2.waitKey(1)
                #timing issue
                time.sleep(0.03)

    def observe(self,visitor):
        frame = self._capture()

        if frame is None:
            print("'OBELISKDIRECTOR No Frame - using Fallback")
            frame = load_image(FALLBACK_IMAGE_PATH)

        #writes to visitor dictionary
        self.run_pipeline(frame, visitor)

    def pause_observe(self, visitor):
        pass
        


    def run_pipeline(self,frame,visitor):
        
        #store in dictionary
        visitor["camera_frame"] = frame

        print("Detecting Body, Face , Hands...")

        #parsed from mediapipe
        detected_results = orchestrate_detection_pipeline(frame , self.body_detector, self.face_detector , self.hand_detector , self.gesture_recognizer )
        intepreted_results = interpret_all_mediapipe_detection(detected_results)

        region_crop = extract_coordinates(detected_results , frame) # for specific region crop
        hsv_crop = cv2.cvtColor(region_crop , cv2.COLOR_BGR2HSV)



        #writing to visitor state dict
        visitor["face_detected"] = intepreted_results["face_detected"]
        visitor["face_orientation"] = intepreted_results["face_orientation"]
        visitor["body_detected"] = intepreted_results["body_detected"]
        visitor["person_count"] = intepreted_results["person_count"]
        visitor["gesture_detected"] = intepreted_results["gesture"] if intepreted_results["gesture"] else None

        # print("Body Results:", detected_results["body"].pose_landmarks)
        # print("Face Results:", detected_results["face"].face_landmarks)
        # print("Hand Results:", detected_results["hand"].hand_landmarks)
        # print("Gesture Results:" , detected_results["gesture"].gestures)

        print("Face Detected:", visitor["face_detected"])
        print("Face Orientation:", visitor["face_orientation"])
        print("Body Detected:", visitor["body_detected"])
        print("Person Count:" , visitor["person_count"])
        print("Gesture Detected:" ,  visitor["gesture_detected"])


        #extracting color values in crop
        print("Extracting Colors..")
        color_results = extract_color(hsv_crop)
        
        visitor["color_saturation"] = color_results["average_saturation"]
        visitor["color_value"] = color_results["average_value"]
        visitor["color_hue"] = color_results["dominant_hue"]


        print("Categorising Results...")
        #classification
        categorised = classify(color_results)
        visitor["hue_category"] = categorised["hue_category"]
        visitor["brightness"] = categorised["brightness"]

        # #selected elements / pngs
        # selection = select(categorised)
        # visitor["selected_elements"] = selection
        
        #later for memory?

    def _return_visitor( self , visitor):
        return visitor

    def select_elements(self,visitor):
        select(visitor)
        print("Selected Elements:" , visitor["selected_elements"] )

    def composite_selphy_card(self,visitor):
        elements = visitor["selected_elements"]
        output_image = composite_elements(elements)

        return output_image
    
    def prepare_selphy_card_print(self,visitor):
        #output_image.save("test/output.png")
        if DEV_MODE:
            img = Image.open(visitor["output_path"])
            img.show()
        else:
            self._print_selphy_card(visitor)


    def _print_selphy_card(self, visitor):
        
        #send output image to Selphy via CUPS
        try:
            filepath = visitor["output_path"]
            print(f"[TEST] Would print: {filepath}")
            #reset CUPS connection to printer
            subprocess.run(["sudo" , "cupsdisable" , SELPHY_PRINTER_NAME] , check=False)
            time.sleep(2)
            subprocess.run(["sudo" , "cupsenable" , SELPHY_PRINTER_NAME] , check=False)
            time.sleep(2)


            #output_image.save(filepath)
            result = subprocess.run(["lp" , "-d", 
                                     SELPHY_PRINTER_NAME , filepath] , 
                                     check=True , 
                                     capture_output=True , 
                                     text = True)

            print("Selphy Print Sent Successful")

            print("Printing in Progress - Wait....")
            time.sleep(SELPHY_PRINT_COOLDOWN)
            #subprocess.run(["cancel", "-a", SELPHY_PRINTER_NAME], check=False)
            print("Selphy Print Job Completed")    
        except Exception as e:
            print(f"Selphy print failed: {e}")

    def _stop_camera(self):
        self.stop_watching() #stop thread before stopping camera
        self.camera.stop()

