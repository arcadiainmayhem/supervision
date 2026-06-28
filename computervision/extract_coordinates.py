from core.installation_constants import *



def extract_coordinates(mp_results , image):
    IMG_HEIGHT, IMG_WIDTH = image.shape[:2]
    
    body = mp_results["body"]
    
    #guard against crashing when no body detected
    if not body.pose_landmarks:
        return _fallback_crop(image)

    try:
        landmarks = body.pose_landmarks[0]

        #assign to landmark points
        left_shoulder = landmarks[11]
        right_shoulder = landmarks[12]

        #just use fallback crop
        if left_shoulder.visibility < 0.6 or right_shoulder.visibility < 0.6 :
            return _fallback_crop(image)

        left_x = int(left_shoulder.x * IMG_WIDTH)
        right_x = int(right_shoulder.x * IMG_WIDTH)
        top_y = int(min(left_shoulder.y , right_shoulder.y) * IMG_HEIGHT)

        
        shoulder_width = abs(right_x - left_x)
        pad_x = int(shoulder_width * 0.15)
        chest_height = int(shoulder_width * 1.5)

        x_min = max(0,min(left_x , right_x)- pad_x)
        x_max = min(IMG_WIDTH , max(left_x , right_x) + pad_x)
        y_min = max (0,top_y)
        y_max = min(IMG_HEIGHT , top_y + chest_height)

        cropped = image[y_min : y_max , x_min : x_max]

        if cropped.size == 0:
            return _fallback_crop(image)
        
        print (f"[MEDIAPIPE][EXTRACT] Shoulder Crop : ({x_min},{y_min} to ({x_max} , {y_max}))")
        return cropped
    
    except Exception as e:
        print(f"[MEDIAPIPE][EXTRACT] Error during Crop {e}")
        return _fallback_crop(image)

def _fallback_crop(image):
    IMG_HEIGHT,IMG_WIDTH = image.shape[:2]

    middle_start = int(IMG_WIDTH * MIDDLE_REGION_START)
    middle_end = int(IMG_WIDTH * MIDDLE_REGION_END)
    print("[MEDIAPIPE][EXTRACT] No Body Detected - Using Fallback Center Crop")
    return image[middle_start : middle_end , : ]