

from hardware.config import *


DEV_MODE = True

if not DEV_MODE:
    import RPi.GPIO as GPIO
else:
    import keyboard





def start(on_press):
    if DEV_MODE:
        print("Dev mode - press SPACE to trigger")
        keyboard.add_hotkey('space',on_press)
        print("Button Listener Ready")
    else:
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(BUTTON_TRIGGER_PIN, GPIO.IN , pull_up_down= GPIO.PUD_UP)

        GPIO.add_event_detect(
            BUTTON_TRIGGER_PIN,
            GPIO.FALLING,
            callback= on_press,
            bouncetime=BUTTON_BOUNCE_TIME
        )
        print("Button Listener Ready")