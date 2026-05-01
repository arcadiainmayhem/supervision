import mediapipe as mp
import cv2
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import os

MODEL_PATH = "computervision/mediapipe/detection/face_landmarker.task"
print("MediaPipe version:", mp.__version__)
print("File size:", os.path.getsize(MODEL_PATH), "bytes")

base_options = python.BaseOptions(model_asset_path=MODEL_PATH)
options = vision.FaceLandmarkerOptions(
    base_options=base_options,
    num_faces=5,
    output_face_blendshapes=True,
    min_face_detection_confidence=0.1,
    min_face_presence_confidence=0.1,
    min_tracking_confidence=0.1
)
detector = vision.FaceLandmarker.create_from_options(options)

image = cv2.imread("test/5.jpg")
print("Image loaded:", image is not None)
if image is not None:
    print("Image shape:", image.shape)

rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
result = detector.detect(mp_image)
print("Faces detected:", len(result.face_landmarks))