from core.scorecard_constants import *



def intepret_expression (visitor):

    expression_score = 0

    #from classifier - might need to read from visitor dict
    hue_category =   visitor["hue_category"] 
    brightness = visitor["brightness"]
    saturation_raw = visitor["color_saturation"]
    

    #from visitor dict
    current_gesture = visitor["gesture_detected"]



    #HUE + BRIGHTNESS SCORING

    #COLOR
    hue_quality = HUE_QUALITY.get(hue_category , HUE_QUALITY["neutral"])
    brightness_quality = BRIGHTNESS_QUALITY.get(brightness, BRIGHTNESS_QUALITY["medium"])
    saturation_quality = min(saturation_raw / 255, 1.0) #distill to 0 -> 1 , clamped

    #total for color axis
    color_score = (hue_quality + brightness_quality + saturation_quality) / 3

    #GESTURE SCORING
    gesture_score = EXPRESSION_GESTURES.get(current_gesture , EXPRESSION_GESTURES["Unknown"])

    #==LABEL
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


    expression_score = (
        color_score * EXPRESSION_W_COLOR +
        gesture_score * EXPRESSION_W_GESTURE
    )


    visitor["expression_score"] = expression_score
    visitor["expression_label"] = label


