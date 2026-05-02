
from computervision.core.classifier_constants import *

def classify(extracted):

    saturation = extracted["average_saturation"]
    hue = extracted["dominant_hue"]
    value = extracted["average_value"]


    #hue categorisation
    if saturation <= SAT_NEUTRAL_MAX:
        hue_category = "neutral"
    elif hue < HUE_WARM_MAX:
        hue_category = 'warm'
    elif hue < HUE_COOL_MAX:
        hue_category = 'cool'
    else:
        hue_category = 'neutral'


    #brightness calculation
    if value < VALUE_DARK_MAX:
        brightness = 'dark'
    elif value > VALUE_LIGHT_MIN:
        brightness = "light"
    else:
        brightness = "medium"


    return {
        'hue_category' : hue_category ,
        'brightness' : brightness
    }