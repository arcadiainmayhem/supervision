
import os

import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision


from computervision.mediapipe.detection.bodydetection import detect_body , setup_body_object
from computervision.mediapipe.detection.facedetection import detect_face , setup_face_object
from computervision.mediapipe.detection.handdetection import detect_hand , setup_hand_object
from computervision.mediapipe.detection.gesture_recognizer import detect_gesture , setup_gesture_object
#Configuring MP to run
BaseOptions = mp.tasks.BaseOptions



def orchestrate_detection_pipeline(image , body_detector, face_detector , hand_detector , gesture_recognizer):
 
    #orchestrating pose detection results
    body_detection_result = detect_body(image , body_detector)
    face_detection_result = detect_face(image , face_detector)
    hand_detection_result = detect_hand(image , hand_detector)
    gesture_detected_and_classified_results = detect_gesture(image , gesture_recognizer)

    return {
        "body": body_detection_result,
        "face" : face_detection_result,
        "hand" : hand_detection_result,
        "gesture" : gesture_detected_and_classified_results
    }