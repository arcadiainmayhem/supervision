#holds visitor variables
from datetime import datetime

def create_visitor_state(visitor_number):

    now = datetime.now()

    return {

    #General & Administrative
    #identity
    "visitor_number" : visitor_number,
    "fallback_used" : False,
    #Observation
    "camera_frame" : None,
    "detected_results" : None,
    #Passive Observation 

    "stillness_variable" : 999.0,
    "dwell_count" : 0,  
    
    #Taken and placed in here from Extractor
    "color_saturation": 0,
    "color_hue": 0,
    "color_value": 0,

    #Mediapipe Detection
    "face_detected" : False,
    "face_orientation" : None,

    "body_detected" : False,
    "person_count" : None,

    "hand_detected" : False,

    "gesture_detected": None,

    #Esoteric
    "moon_phase" : None,
    "element" : None,
    "numerology" : None,

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

    #For Final Output
    "output_type" : None,
    "output_path" : None,
    "selected_elements" : None,
    "assembled_slip" : None,
    
    #--PRESENCE AXIS
    "presence_score" : None,
    "presence_label" : None,
    #--CONTEXT AXIS
    "context_score" : None,
    "context_label" : None,
    #--EXPRESSION AXIS
    "expression_score" : None,
    "expression_label" : None,
    #--TIME AXIS
    "time_score" : None,
    "time_label" : None,
    #--For Feature Decision
    "unlocked_rarity_tier" : None,

    "printed" : False,
}