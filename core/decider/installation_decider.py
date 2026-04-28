

SELPHY_THRESHOLD = 0.8



def decide_score(visitor):

    visitor_score = 0


    #score deciders
    if visitor["face_detected"]: visitor_score += 0.3
    if visitor["body_detected"]: visitor_score += 0.1
    if visitor["hand_detected"]: visitor_score += 0.2

    #Specific pose detection

    #specific hand gesture detection

    #hue category
    if visitor["hue_category"] == "warm":
        visitor_score += 0.12
    elif visitor["hue_category"] == "cool":
        visitor_score += 0.13
    elif visitor["hue_category"] == "neutral":
        visitor_score += 0.09
    #brightness category
    if visitor["brightness"] == "dark":
        visitor_score += 0.12
    elif visitor["brightness"] == "light":
        visitor_score += 0.13

    #Dwell Time

    #Energy 

    visitor["satisfaction_score"] = visitor_score

    #decide output
    output_type = _score_to_print_output(visitor_score)

    return {
        "printer_output_type" : output_type,
        "satisfaction_score" : visitor_score,
    }


def _score_presence(visitor): # face, body, hands
    pass
def _score_colour(visitor):   # hue, brightness  
    pass
def _score_behaviour(visitor): # dwell time, energy
    pass
def _score_context():          # moon, date
    pass

def _score_to_print_output(score):
    
    if score >= SELPHY_THRESHOLD:
        return "selphy"
    else:
        return "thermal"