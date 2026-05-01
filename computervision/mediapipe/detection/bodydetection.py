
import os
import cv2
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
# from mediapipe.tasks.python.vision import drawing_utils
# from mediapipe.tasks.python.vision import drawing_styles
from mediapipe.tasks.python import vision


MODEL_PATH = os.path.join(os.path.dirname(__file__), "pose_landmarker_full.task")


#Create Pose Landmarker Object
def setup_body_object():
    base_options = python.BaseOptions(model_asset_path = MODEL_PATH )

    options = vision.PoseLandmarkerOptions(
        base_options = base_options,
        min_pose_detection_confidence = 0.5,
        min_pose_presence_confidence = 0.5,
        min_tracking_confidence = 0.5,
        )
    detector = vision.PoseLandmarker.create_from_options(options)

    return detector
#mediapipe wants RGB , not BGR
def detect_body(image, detector):

    rgb = cv2.cvtColor(image , cv2.COLOR_BGR2RGB)
    #wrap values in mp.Image because MP doesnt want raw pixels, wants them in its own coontainer that it knows how to work with
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data = rgb)

    #detect + contains pose landmark from input image
    detection_result = detector.detect(mp_image)

    #process detection result , visualisation only
    #annotated_image = draw_landmarks_on_image(rgb , detection_result)

    #detected_result = cv2.cvtColor(annotated_image, cv2.COLOR_RGB2BGR)

    return detection_result


# def draw_landmarks_on_image(rgb_image , detection_result):

#     pose_landmarks_list = detection_result.pose_landmarks
#     annoted_image = np.copy(rgb_image)

#     pose_landmark_style = drawing_styles.get_default_pose_landmarks_style()
#     pose_connection_style = drawing_utils.DrawingSpec(color = ( 0 , 255 , 0 ), thickness = 2)
    
#     for pose_landmarks in pose_landmarks_list:
        
#         drawing_utils.draw_landmarks(
#             image = annoted_image,
#             landmark_list = pose_landmarks,
#             connections = vision.PoseLandmarksConnections.POSE_LANDMARKS,
#             landmark_drawing_spec = pose_landmark_style,
#             connection_drawing_spec = pose_connection_style
#         )

#     return annoted_image