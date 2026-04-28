
import os

import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision


from computervision.mediapipe.detection.posedetection import detect_pose , setup_pose_object

#Configuring MP to run
BaseOptions = mp.tasks.BaseOptions



def orchestrate_detection_pipeline(image , detector):
 
    #orchestrating pose detection results
    pose_detection_result = detect_pose(image , detector)


    return {
        "pose":pose_detection_result
    }