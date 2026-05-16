import cv2
import numpy as np
import mediapipe as mp
from mediapipe import solutions
import platform


if platform.system() == "Linux":
    from mediapipe.framework.formats import landmark_pb2



def draw_detections(frame , detected_results):


    annotated = np.copy(frame)



    _draw_body(annotated , detected_results["body"])
    _draw_face(annotated , detected_results["face"])
    _draw_hands(annotated , detected_results["hand"])

    return annotated

def _draw_body(frame , body_result):

    if not body_result.pose_landmarks:
        return
    

    for pose_landmarks in body_result.pose_landmarks:
        #convert Tasks Landmarks to protobuf format for drawing_utils
        landmark_list = landmark_pb2.NormalizedLandmarkList()
        landmark_list.landmark.extend([
            landmark_pb2.NormalizedLandmark(x = lm.x , y = lm.y , z=lm.z)
            for lm in pose_landmarks
        ])

        solutions.drawing_utils.draw_landmarks(
            frame,
            landmark_list,
            solutions.pose.POSE_CONNECTIONS,
            solutions.drawing_styles.get_default_pose_landmarks_style()
        )

def _draw_face(frame, face_result):
    if not face_result.face_landmarks:
        return

    for face_landmarks in face_result.face_landmarks:
        landmark_list = landmark_pb2.NormalizedLandmarkList()
        landmark_list.landmark.extend([
            landmark_pb2.NormalizedLandmark(x=lm.x, y=lm.y, z=lm.z)
            for lm in face_landmarks
        ])

        solutions.drawing_utils.draw_landmarks(
            frame,
            landmark_list,
            solutions.face_mesh.FACEMESH_TESSELATION,
            landmark_drawing_spec=None,
            connection_drawing_spec=solutions.drawing_styles.get_default_face_mesh_tesselation_style()
        )


def _draw_hands(frame, hand_result):
    if not hand_result.hand_landmarks:
        return

    for hand_landmarks in hand_result.hand_landmarks:
        landmark_list = landmark_pb2.NormalizedLandmarkList()
        landmark_list.landmark.extend([
            landmark_pb2.NormalizedLandmark(x=lm.x, y=lm.y, z=lm.z)
            for lm in hand_landmarks
        ])

        solutions.drawing_utils.draw_landmarks(
            frame,
            landmark_list,
            solutions.hands.HAND_CONNECTIONS,
            solutions.drawing_styles.get_default_hand_landmarks_style(),
            solutions.drawing_styles.get_default_hand_connections_style()
        )