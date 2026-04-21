import cv2
import numpy as np
from core.constants import *

def extract_color(hsv_region):

    #mask out low saturation pixels
    saturation = hsv_region[ : , : , 1]
    #calculate average saturation
    average_saturation = np.mean(saturation)
    #create mask where saturation is above threshold
    mask = (saturation > SAT_MIN_THRESHOLD).astype(np.uint8) * 255 #needs to be uint8 for opencv to accept , *255 converts to true / false to 255 / 0
    #calculate hue histogram on masked pixels
    hue_histogram = cv2.calcHist([hsv_region], [0] , mask , [180], [0,180] )

    #find dominant hue in array
    dominant_hue = np.argmax(hue_histogram)

    #average value - use numpy average
    average_value = np.mean(hsv_region[: , : , 2])


    return {
        "dominant_hue" : dominant_hue, 
        "average_value": average_value,
        "average_saturation" : average_saturation
    }