from core.scorecard_constants import *



def intepret_expression (visitor):

    expression_score = 0

    #from classifier - might need to read from visitor dict
    hue_category =   visitor["hue_category"] 
    brightness = visitor["brightness"]

    #from visitor dict
    current_gesture = visitor["gesture_detected"]

    #HUE + BRIGHTNESS SCORING

    if hue_category == "warm":
        expression_score += SCORE_HUE_WARM
    elif hue_category == "cool":
        expression_score += SCORE_HUE_COOL
    elif hue_category == "neutral":
        expression_score += SCORE_HUE_NEUTRAL
    else:
        expression_score += SCORE_HUE_NEUTRAL
    
    if brightness == "light":
        expression_score += SCORE_BRIGHTNESS_LIGHT
    elif brightness == "dark":
        expression_score += SCORE_BRIGHTNESS_DARK
    elif brightness == "medium":
        expression_score += SCORE_BRIGHTNESS_MEDIUM
    else:
        expression_score += SCORE_BRIGHTNESS_MEDIUM

    if current_gesture and current_gesture != "Unknown":
        label = ExpressionLabel.EXPRESSIVE
    elif hue_category == "warm" and brightness == "light":
        label = ExpressionLabel.WARM_LIGHT
    elif hue_category == "warm" and brightness == "dark":
        label = ExpressionLabel.WARM_DARK
    elif hue_category == "cool" and brightness == "light":
        label = ExpressionLabel.COOL_LIGHT
    elif hue_category == "cool" and brightness == "dark":
        label = ExpressionLabel.COOL_DARK
    elif hue_category == "neutral" and brightness == "medium":
        label = ExpressionLabel.NEUTRAL
    elif hue_category == "neutral" and brightness in ("light" , "dark"):
        label = ExpressionLabel.NEUTRAL
    else:
        label = ExpressionLabel.NEUTRAL

    #GESTURE MEANING SCORING
    if current_gesture == "Closed_Fist":
        expression_score += SCORE_GESTURE_CLOSED_FIST
    elif current_gesture == "Open_Palm":
        expression_score += SCORE_GESTURE_OPEN_PALM
    elif current_gesture == "Pointing_Up":
        expression_score += SCORE_GESTURE_POINTING_UP
    elif current_gesture == "Thumbs_Down":
        expression_score += SCORE_GESTURE_THUMBS_DOWN
    elif current_gesture == "Thumbs_Up":
        expression_score += SCORE_GESTURE_THUMBS_UP
    elif current_gesture == "Victory":
        expression_score += SCORE_GESTURE_VICTORY
    elif current_gesture == "ILoveYou":
        expression_score += SCORE_GESTURE_LOVE
    elif current_gesture == "Unknown":
        expression_score += SCORE_GESTURE_UNKNOWN
    else:
        expression_score += SCORE_GESTURE_UNKNOWN

    visitor["expression_score"] = expression_score
    visitor["expression_label"] = label
