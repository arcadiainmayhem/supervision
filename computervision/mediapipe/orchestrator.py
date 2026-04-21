
import os

import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

from computervision.imageloader import load_image
from computervision.mediapipe.detection.posedetection import detect_pose , setup_pose_object

#Configuring MP to run
BaseOptions = mp.tasks.BaseOptions



def orchestrate_pipeline(image):
 
    detected = setup_pose_object()
    
    pose_detection_result = detect_pose(image , detected)


    return {
        "pose":pose_detection_result
    }