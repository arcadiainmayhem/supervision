

from core.scorecard_constants import *



#for face body , gets dict pass in after intepreted

def interpret_presence(visitor):

    presence_score = 0

    face_detected = visitor["face_detected"]
    face_orientation = visitor["face_orientation"]
    body_detected = visitor["body_detected"]
    person_count = visitor["person_count"] 

    #==FACE 
    #CHECK FOR FACE
    if face_detected: 
        face_score = FACE_ORIENTATION_DIRECTION.get(face_orientation, FACE_ORIENTATION_DIRECTION["forward"])
    else:
        face_score = 0

    #BODY
    body_score = 1.0 if body_detected else 0.0

    #COUNT
    if person_count == 1:
        count_score = PERSON_COUNT_SOLO
    elif 2 <= person_count <= 4:
        count_score = PERSON_COUNT_PAIR
    elif person_count >= 5:
        count_score = PERSON_COUNT_CROWD
    else:
        count_score = PERSON_COUNT_NONE

    #GETS TOTAL PRESENCE SCORE
    presence_score = (
        face_score * PRESENCE_W_FACE +
        body_score * PRESENCE_W_BODY +
        count_score * PRESENCE_W_COUNT
    ) #gets normalised 


    #DETERMINE PRESENCE LABEL
    if not face_detected and not body_detected:
        label = PresenceLabel.ABSENT
    elif not face_detected and body_detected:
        label = PresenceLabel.PARTIAL
    elif face_detected and face_orientation == "down":
        label = PresenceLabel.DEFERENTIAL
    elif face_detected and face_orientation in ("left" , "right" , "up" ):
        label = PresenceLabel.AVERTED
    elif person_count >= 5:
        label = PresenceLabel.CROWD
    else:
        label = PresenceLabel.PRESENT #face detected, forward


    visitor["presence_score"] = presence_score
    visitor["presence_label"] = label




