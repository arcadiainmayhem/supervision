#holds visitor variables
from datetime import datetime

def create_visitor_state(visitor_number):

    now = datetime.now()

    return {
    #General & Administrative
    #identity
    "number" : visitor_number,

    #Observation
    "camera_frame" : None,
    "color_saturation": 0,
    "color_hue": 0,
    "color_value":0,

    #Poses
    # "pose_landmarks" : None,
    # "detected_regions" : None,

    "face_detected" : False,
    "face_orientation" : None,

    "body_detected" : False,
    "person_count" : None,

    "hand_detected" : False,

    "gesture_detected": None,

    #Extracted from Vision - Aura

    "energy" : None,
    "nervousness":  None ,
    "calmness": None,

    #Classification
    "hue_category" : None,
    "brightness" : None,

    #Time
    "timestamp" : now,
    "datestamp" : now,
    "start_time" : now,
    "end_time" : None,
    #decider - output
    "satisfaction_score": None,
    "satisfaction_met" : False,

    "output_type" : None,
    "selected_elements" : None,
}