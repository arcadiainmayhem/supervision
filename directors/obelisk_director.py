import time
import numpy as np
import cv2
import threading
import subprocess
import requests
from PIL import Image
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
from computervision.mediapipe.detection.drawing_utils import draw_detections

from obelisk_compositor.obelisk_card_selector import select
from obelisk_compositor.obelisk_card_compositor import composite_elements


from monitoring import status_logger
#Observe

#Accumulate

#Points / Produces output

class ObeliskDirector():

    def __init__(self):
        #runs once
        #obelisk variables
        self.isWatching = False
    
        #printing state flag     
        self.isPrinting = False
        #camera availability
        self.camera_available = True
        self.lastest_frame = None
        self._frame_lock = threading.Lock()

        #passive metrics 
        self._prev_frame = None
        self.stillness_variable = 999.0
        self.dwell_count = 0
        self._variance_history = []
        self._variance_window = 10

        self._stream_thread = threading.Thread(target= self._stream_loop , daemon=True)
        self._stream_thread.start()
        #threadings 

        #start health check
        self.health_check_thread = threading.Thread(target= self._camera_health_check_loop)
        self.health_check_thread.daemon = True
        self.health_check_thread.start()

        

        #current running data
        self.current_observation = None
     

        #initilaise mediapose objects
        self.body_detector = setup_body_object()
        self.face_detector = setup_face_object()
        self.hand_detector = setup_hand_object()
        self.gesture_recognizer = setup_gesture_object()

    def _stream_loop(self):
        while True: #runs forever
            try:
                url = f"http://{CAMERA_PI_IP}:{CAMERA_PI_PORT}/stream"

                print(f"[OBELISKDIRECTOR][STREAM] Attempting Connection to {url}")

                response = requests.get(url , stream= True , timeout = 10) #opens one connection to stream
                print("[OBELISKDIRECTOR][STREAM] Stream Connected Successfully")
                #[UPDATE STATUS]
                status_logger.update_status("camera" , "online")
                self.camera_available = True

                for frame in self._iter_mjpeg(response): #each iteration 
                    with self._frame_lock: #when it has the lock , locks the room
                        self.lastest_frame = frame #update latest frame
                        self._update_passive_metrics(frame) #update passive metrics
                #room unlocks automatically
            except Exception as e:
                if self.camera_available:
                    print(f"[OBELISKDIRECTOR][STREAM] Stream Lost: {e}")
                    status_logger.update_status("camera","unreachable")
                self.camera_available = False
                print(f"[OBELISKDIRECTOR][STREAM] Stream Attempting Reconnection in  {CAMERA_HEALTH_CHECK_INTERVAL}")

                time.sleep(CAMERA_STREAM_RECONNECTION_INTERVAL) # wait then reconnect


    def _iter_mjpeg(self , response):
        #Parse MJPEG multipart stream, yield decoded frames as numpy arrays.
        buffer = bytes()
        for chunk in response.iter_content(chunk_size=4096):
            buffer += chunk
            start = buffer.find(b'\xff\xd8')  # JPEG start
            end = buffer.find(b'\xff\xd9')    # JPEG end
            if start != -1 and end != -1:
                jpg = buffer[start:end+2]
                buffer = buffer[end+2:]
                arr = np.frombuffer(jpg, dtype=np.uint8)
                frame = cv2.imdecode(arr, cv2.IMREAD_COLOR)
                if frame is not None:
                    yield frame

    def _update_passive_metrics(self,frame):
        #called from inside lock
        self.dwell_count += 1

        if self._prev_frame is not None:
            diff = cv2.absdiff(frame , self._prev_frame)
            variance = float(np.mean(diff))

            self._variance_history.append(variance)
            if len(self._variance_history) > self._variance_window:
                self._variance_history.pop(0)

            self.stillness_variable = sum(self._variance_history) / len(self._variance_history)

        self._prev_frame = frame

    def _camera_health_check_loop(self):
        while True:
            try:
                response = requests.get(
                    f"http://{CAMERA_PI_IP}:{CAMERA_PI_PORT}/health",
                    timeout=3
                )
                if response.status_code == 200:
                    if not self.camera_available:
                        print("[OBELISKDIRECTOR] Camera Pi back online")
                        status_logger.update_status("camera","online")
                    self.camera_available = True

                else:
                    if self.camera_available:
                        print(f"[OBELISKDIRECTOR] Camera Pi unhealthy: {response.status_code}")
                    self.camera_available = False

            except Exception as e:
                if self.camera_available:
                    print(f"[OBELISKDIRECTOR] Camera Pi unreachable {e}")
                    status_logger.update_status("camera","unreachable")
                self.camera_available = False
            
            time.sleep(CAMERA_HEALTH_CHECK_INTERVAL)

    def capture(self):

        if DEV_MODE:
            return load_image(FALLBACK_IMAGE_PATH)
        
        with self._frame_lock:
            frame = self.lastest_frame


        if frame is None:
            print("[OBELISKDIRECTOR] No frame yet - using fallback")
            return load_image(FALLBACK_IMAGE_PATH)
        
        return frame

    def observe(self,visitor):
        print(f"[OBELISKDIRECTOR][OBSERVE] Triggered for visitor {visitor['visitor_number']}")
        try:
            with self._frame_lock: #locks the room
                frame = self.lastest_frame #copy whatever is there
                visitor["dwell_count"] = self.dwell_count
                visitor["stillness_variable"] = self.stillness_variable
                self.dwell_count = 0 #reset for next visitor
            print(f"[OBELISKDIRECTOR][OBSERVE] dwell_count : {visitor['dwell_count']} | stillness : {visitor['stillness_variable']:.2f}")

            if frame is None:
                print(f"[OBELISKDIRECTOR][OBSERVE] No frame available, using Fallback")
                frame = load_image(FALLBACK_IMAGE_PATH)
            else:
                print(f"[OBELISKDIRECTOR][OBSERVE] Frame grabbed - Shape : {frame.shape}")

            #outside of the lock - stream thread can write again
            self.run_pipeline(frame , visitor)

            if SHOW_DETECTIONS:
                annotated = draw_detections(visitor["camera_frame"],visitor["detected_results"] )
                cv2.imshow("Detection Preview",annotated)
                cv2.waitKey(1)

        except Exception as e:
            print(f"[OBELISKDIRECTOR][OBSERVE] Failed: {e}")
            visitor["camera_frame"] = None
            visitor["dwell_count"] = 0
            visitor["stillness_variable"] = 999.0

    def pause_observe(self, visitor):
        pass
        


    def run_pipeline(self,frame,visitor):
        
        #store in dictionary
        visitor["camera_frame"] = frame

        print("Detecting Body, Face , Hands...")

        #parsed from mediapipe
        detected_results = orchestrate_detection_pipeline(frame , self.body_detector, self.face_detector , self.hand_detector , self.gesture_recognizer )
        intepreted_results = interpret_all_mediapipe_detection(detected_results)

        visitor["detected_results"] = detected_results

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
        if DEV_MODE:
            img = Image.open(visitor["output_path"])
            img.show()
            return True
        else:
            return self._print_selphy_card(visitor)


    def _print_selphy_card(self, visitor):

        #send output image to Selphy via CUPS
        try:
            filepath = visitor["output_path"]

            if SKIP_PRINT:
                print(f"[OBELISKDIRECTOR] SKIP_PRINT enabled — skipping: {filepath}")
                return True

            print(f"[TEST] Would print: {filepath}")
            
            #[UPDATE STATUS OF PRINTER]
            status_logger.update_status("printer" , "resetting")

            #reset CUPS connection to printer so printer wont get stuck
            subprocess.run(["sudo" , "cupsdisable" , SELPHY_PRINTER_NAME] , check=False)
            time.sleep(2)
            subprocess.run(["sudo" , "cupsenable" , SELPHY_PRINTER_NAME] , check=False)
            time.sleep(2)

            #check printer status via CUPS - generates readable lines
            check = subprocess.run(["lpstat" , 
                                    "-p" ,
                                    SELPHY_PRINTER_NAME,],
                                    capture_output = True,
                                    text = True)

            printer_status = check.stdout.strip()
            print(f"[SELPHYPRINTER] Printer Status : {printer_status}")
   
            #quits queue if printerstatus fails
            if "error" in printer_status.lower() or "disabled" in printer_status.lower():
                status_logger.update_status("printer" , "error")
                status_logger.log_error("Selphy" ,printer_status)
                visitor["printed"] = False
                return False

            #send to printer to print if status is okay
            subprocess.run(["lp" , "-d", 
                                     SELPHY_PRINTER_NAME , 
                                     filepath] , 
                                     check=True , 
                                     capture_output=True , 
                                     text = True)

            print("Selphy Print Sent Successful")
            #[UPDATE STATUS OF PRINTER]
            status_logger.update_status("printer" , "printing")

            print("Printing in Progress - Wait....")

            time.sleep(SELPHY_PRINT_COOLDOWN)

            #flip printed key in visitor state to true

            visitor["printed"] = True

            #[UPDATE STATUS OF PRINTER]
            status_logger.update_status("printer" , "ready")
            
            #subprocess.run(["cancel", "-a", SELPHY_PRINTER_NAME], check=False)
            print("Selphy Print Job Completed")  

            return True
            
        except Exception as e:
            visitor["printed"] = False
            #[UPDATE STATUS OF PRINTER]
            status_logger.update_status("printer" , "eror")
            status_logger.log_error("Selphy" , str(e))
            print(f"Selphy print failed: {e}")

            return False

