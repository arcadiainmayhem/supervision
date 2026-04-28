
from core.installation_constants import *
import cv2
import numpy as np






def load_image(path):
    img_bgr = cv2.imread(path)

    #Silently fail if cant find
    if img_bgr is None:
        raise FileNotFoundError(f"Could Not Load Image: {path}")

    return img_bgr


def get_region(bgr):
    
    #derive height and width from image
    height , width = bgr.shape[:2]

    #get pixel values for middle portion
    middle_start = int(height * MIDDLE_REGION_START) 
    middle_end = int(height * MIDDLE_REGION_END)

    slicedRegion = bgr[middle_start : middle_end , :]


    return slicedRegion