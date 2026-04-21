import time
from hardware.button_listener import start

from hardware.camera.camera_constants import *
from core.constants import *
from computervision.extractor import extract_color
from computervision.classifier import classify
from compositor.selector import select
from compositor.compose import composite_elements
from computervision.extract_coordinates import extract_coordinates
from computervision.mediapipe.orchestrator import orchestrate_pipeline
from hardware.camera.camera_manager import CameraManager

#runs once
camera= CameraManager()
#start camera
camera.start()

def on_press(channel = None):
    if USE_CAMERA:
        #capture live image from camera if camera is connected
        captured_frame = camera.preview()
    else:
        captured_frame = camera.capture()

    #run computer vision pipeline

    orchestrated = orchestrate_pipeline(captured_frame)
    # Get Region
    torso_crop = extract_coordinates(orchestrated , captured_frame)
    #composite elements 
    results = extract_color(torso_crop)

    categorised = classify(results)

    selection = select(categorised)
    
    output = composite_elements(selection)


    #save the card  


    #send to printer    
    print(results)
    print(categorised)
    print(selection)
    print(output)
   
   
    output.show()

start(on_press)

print("Running!")

while True:
    time.sleep(0.1)