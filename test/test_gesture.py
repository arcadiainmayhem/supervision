import mediapipe as mp
import cv2
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import os

MODEL_PATH = "computervision/mediapipe/detection/gesture_recognizer.task"
print("MediaPipe version:", mp.__version__)
print("File size:", os.path.getsize(MODEL_PATH), "bytes")

base_options = python.BaseOptions(model_asset_path=MODEL_PATH)
options = vision.GestureRecognizerOptions(
        base_options = base_options,
        num_hands = 4,
        )

detector = vision.GestureRecognizer.create_from_options(options)

image = cv2.imread("test/6.jpg")
print("Image loaded:", image is not None)
if image is not None:
    print("Image shape:", image.shape)

rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
result = detector.recognize(mp_image)

print("Gestures detected:", len(result.gestures) , result.gestures[0][0].category_name)