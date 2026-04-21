from core.constants import *

def extract_coordinates(mp_results , image):
    
    pose = mp_results["pose"]
    
    #guard against crashing when no pose
    if not pose.pose_landmarks:
        IMG_HEIGHT, IMG_WIDTH = image.shape[:2]

        print("No Pose Detected - using fallback")
        middle_start = int(IMG_HEIGHT * MIDDLE_REGION_START) 
        middle_end = int(IMG_HEIGHT * MIDDLE_REGION_END)

        return image[middle_start : middle_end, :]
 
    landmarks = pose.pose_landmarks[0]

    #assign to landmark points
    left_shoulder = landmarks[12]
    right_shoulder = landmarks[11]
    left_hip = landmarks[24]
    right_hip = landmarks[23]

    IMG_HEIGHT, IMG_WIDTH = image.shape[:2]

    #check visiblity here 
    if (left_shoulder.visibility > 0.7 and
        right_shoulder.visibility > 0.7 and
        left_hip.visibility > 0.7 and
        right_hip.visibility > 0.7):

        #use landmark coordinates
        #pixel coordinates for shoulders and hips
        left_shoulder_px_x = int(left_shoulder.x * IMG_WIDTH )
        left_shoulder_px_y = int(left_shoulder.y * IMG_HEIGHT )

        right_shoulder_px_x = int(right_shoulder.x * IMG_WIDTH )
        right_shoulder_px_y = int(right_shoulder.y * IMG_HEIGHT )

        left_hip_px_x = int(left_hip.x * IMG_WIDTH )
        left_hip_px_y = int(left_hip.y * IMG_HEIGHT )

        right_hip_px_x = int(right_hip.x * IMG_WIDTH )
        right_hip_px_y = int(right_hip.y * IMG_HEIGHT )

        x_min = min(left_shoulder_px_x, left_hip_px_x)
        x_max = max(right_shoulder_px_x, right_hip_px_x)
        y_min = min(left_shoulder_px_y, right_shoulder_px_y)
        y_max = max(left_hip_px_y, right_hip_px_y)

        print("left shoulder: ", left_shoulder_px_x , left_shoulder_px_y)
        print("right shoulder: ", right_shoulder_px_x , right_shoulder_px_y)
        print("left_hip:", left_hip_px_x, left_hip_px_y)
        print("right_hip:", right_hip_px_x, right_hip_px_y)

        cropped = image[y_min:y_max, x_min:x_max]

        return cropped
    
    else:

      #use fallback middle region
      #get pixel values for middle portion

      print("Low visibility - using fallback crop")

      middle_start = int(IMG_HEIGHT * MIDDLE_REGION_START) 
      middle_end = int(IMG_HEIGHT * MIDDLE_REGION_END)

      return image[middle_start : middle_end, :]