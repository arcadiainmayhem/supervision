

from core.scorecard_constants import *



#for face body , gets dict pass in after intepreted

def interpret_presence(visitor):

    presence_score = 0

    face_detected = visitor["face_detected"]
    face_orientation = visitor["face_orientation"]
    body_detected = visitor["body_detected"]
    person_count = visitor["person_count"] 

    #==FACE 
    if face_detected: presence_score += SCORE_FACE_DETECTED 

    if face_orientation == "forward":
        presence_score += SCORE_FACE_FRONT
    elif face_orientation == "left":
        presence_score += SCORE_FACE_LEFT
    elif face_orientation == "right":
        presence_score += SCORE_FACE_RIGHT
    elif face_orientation == "up":
        presence_score += SCORE_FACE_UP
    elif face_orientation == "down":
        presence_score += SCORE_FACE_DOWN
    else:
        presence_score += SCORE_FACE_FRONT


    #BODY
    if body_detected: presence_score += SCORE_BODY_DETECTED 

    if person_count == 1:
        presence_score += SCORE_PERSON_SOLO
    elif 2 <= person_count <= 4 :
        presence_score += SCORE_MULTI_PERSON_2_4
    elif person_count >= 5:
        presence_score += SCORE_MULTI_PERSON_5_PLUS
    else:
        presence_score += SCORE_PERSON_SOLO


    #DETERMINE PRESENCE LABEL
    if not face_detected and not body_detected:
        label = PresenceLabel.ABSENT
    elif not face_detected and body_detected:
        label = PresenceLabel.PARTIAL
    elif face_detected and face_orientation == "down":
        label = PresenceLabel.DEFERENTIAL
    elif face_detected and face_orientation in ("left" , "right" , "up" , "down"):
        label = PresenceLabel.AVERTED
    elif person_count >= 5:
        label = PresenceLabel.CROWD
    else:
        label = PresenceLabel.PRESENT #face detected, forward


    visitor["presence_score"] = presence_score
    visitor["presence_label"] = label




