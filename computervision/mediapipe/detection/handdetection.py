
import os
import cv2
import mediapipe as mp
from mediapipe.tasks import python
# from mediapipe.tasks.python.vision import drawing_utils
# from mediapipe.tasks.python.vision import drawing_styles
from mediapipe.tasks.python import vision


MODEL_PATH_HAND = os.path.join(os.path.dirname(__file__), "hand_landmarker.task")


#Create Hand Landmarker Object
def setup_hand_object():
    base_options = python.BaseOptions(model_asset_path = MODEL_PATH_HAND )

    options = vision.HandLandmarkerOptions(
        base_options = base_options,
        num_hands = 4,
        )
    detector = vision.HandLandmarker.create_from_options(options)

    return detector

#mediapipe wants RGB , not BGR
def detect_hand(image, detector):

    rgb = cv2.cvtColor(image , cv2.COLOR_BGR2RGB)
    #wrap values in mp.Image because MP doesnt want raw pixels, wants them in its own coontainer that it knows how to work with
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data = rgb)
    # print("Hand Image shape:", rgb.shape)
    # print("Hand Image dtype:", rgb.dtype)
    #detect + contains hand landmark from input image


    detection_result = detector.detect(mp_image)



    # print("Hand:" , detection_result)
    # print("Hand model path:", MODEL_PATH_HAND)
    # print("Model exists:", os.path.exists(MODEL_PATH_HAND))
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