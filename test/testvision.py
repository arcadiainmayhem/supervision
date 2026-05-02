

import cv2
import numpy as np
from computervision.imageloader import load_image, get_region
from core.installation_constants import *
from computervision.extractor import extract_color
from computervision.classifier import classify
from obelisk_compositor.obelisk_card_selector import select
from obelisk_compositor.obelisk_card_compositor import composite_elements
from computervision.mediapipe.orchestrator import orchestrate_pipeline
from computervision.extract_coordinates import extract_coordinates

# Load Image


def test_run(image_path):
    bgr = load_image(image_path)
    print("Image Loaded, shape: ", bgr.shape)


    sorted_from_media = orchestrate_pipeline(bgr)

    pose_detection = sorted_from_media["pose"]
    # Get Region
    torso_crop = extract_coordinates(sorted_from_media , bgr)

    #torso_bgr = cv2.cvtColor(sorted_from_media, cv2.COLOR_HSV2BGR)

    results = extract_color(torso_crop)
    
    categorised = classify(results)

    selection = select(categorised)
    
    output = composite_elements(selection)

    print(results)
    print(categorised)
    print(selection)
    print ( output )
   
   
    output.show()

    return output

