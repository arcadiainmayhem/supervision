
import numpy as np




def interpret_all_mediapipe_detection(detected_results):


    face = intepret_face(detected_results["face"])
    body = intepret_body(detected_results["body"])
    gesture = intepret_gesture(detected_results["gesture"])

    return {
        "face_detected" : face["face_detected"],
        "face_orientation" : face["face_orientation"],
        "body_detected" : body["body_detected"],
        "person_count" : body["person_count"],
        "gesture" : gesture["gesture"]
    }

def intepret_face(face_result):
    #check if theres face
    face_detected =  len(face_result.face_landmarks) > 0
    face_direction = None

    if face_detected and face_result.facial_transformation_matrixes:
        matrix = np.array(face_result.facial_transformation_matrixes[0].data).reshape(4,4)

        #yaw - left / right rotation  extracted from matrix
        yaw = np.arctan2(matrix[0][2], matrix[2][2] )* (180 / np.pi)
        pitch = np.arctan2(-matrix[1][2] , np.sqrt(matrix[0][2]**2 + matrix[2][2]**2))* (180 / np.pi)

        if yaw < -15:
            face_direction = "left"
        elif yaw > 15:
            face_direction = "right"
        elif pitch > 15:
            face_direction = "up"
        elif pitch < -15:
            face_direction = "down"
        else:
            face_direction = "forward"

    return {
        "face_detected" : face_detected,
        "face_orientation" : face_direction
    }


def intepret_body(body_result):

    #check if theres body
    person_count =  len(body_result.pose_landmarks) 

    return {
        "body_detected" : person_count > 0,
        "person_count" : person_count
    }




def intepret_gesture(gesture_result):

    gesture = gesture_result.gestures

    if not gesture:
        return { "gesture" : None}

    #take first detected hand gesture
    top_gesture = gesture[0][0].category_name

    return {"gesture" : top_gesture}