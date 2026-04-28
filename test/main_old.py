# import time
# from hardware.button.button_listener import start
# import cv2
# from hardware.camera.camera_constants import *
# from core.installation_constants import *
# from computervision.extractor import extract_color
# from computervision.classifier import classify
# from compositor.selector import select
# from compositor.compose import composite_elements
# from computervision.extract_coordinates import extract_coordinates
# from computervision.mediapipe.orchestrator import orchestrate_detection_pipeline
# from hardware.camera.camera_manager import CameraManager

# #runs once
# camera= CameraManager()
# #start camera
# camera.start()

# def run_pipeline(frame):
#     orchestrated = orchestrate_detection_pipeline(frame)
#     # Get Region
#     torso_crop = extract_coordinates(orchestrated , frame)

#     if torso_crop is None:
#         print("No Person Detected - skipping pipeline")
#         return

#     #composite elements 
#     results = extract_color(torso_crop)

#     categorised = classify(results)

#     selection = select(categorised)
    
#     output = composite_elements(selection)
   
#     print(results)
#     print(categorised)
#     print(selection)
#     print(output)
   
   
#     output.show()

# if DEV_MODE:
#     while True:
#         frame = camera.preview_frame()                 
#         cv2.imshow("Preview" , frame)
#         key = cv2.waitKey(1)
#         if key == 32:
#             cv2.destroyAllWindows()
#             run_pipeline(frame)

# else:
#     from hardware.button.button_listener import start

#     def on_press(channel = None):
#         frame = camera.capture()
#         run_pipeline(frame)

#     start(on_press)
#     print("Running!")

#     while True:
#         time.sleep(0.1)