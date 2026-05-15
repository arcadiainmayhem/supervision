

from hardware.hardware_config import *
from core.installation_constants import DEV_MODE


if not DEV_MODE:
    import RPi.GPIO as GPIO
else:
    import keyboard





def register_trigger_button(on_press):
    if DEV_MODE:
        print("Dev mode - press SPACE to trigger")
        keyboard.add_hotkey('space',on_press)
        print("Trigger Button Ready")
    else:
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(BUTTON_TRIGGER_PIN, GPIO.IN , pull_up_down= GPIO.PUD_UP)

        GPIO.remove_event_detect(BUTTON_TRIGGER_PIN)  # clear buffer + remove old
        
        GPIO.add_event_detect(
            BUTTON_TRIGGER_PIN,
            GPIO.FALLING,
            callback= on_press,
            bouncetime=BUTTON_BOUNCE_TIME
        )
        



def register_shutdown_button(on_press):
    if DEV_MODE:
        print("Dev mode - press SPACE to trigger")
        keyboard.add_hotkey('q',on_press)
        print("Shutdown Button Ready")
    else:
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(SHUTDOWN_TRIGGER_PIN, GPIO.IN , pull_up_down= GPIO.PUD_UP)

        GPIO.add_event_detect(
            SHUTDOWN_TRIGGER_PIN,
            GPIO.FALLING,
            callback= on_press,
            bouncetime=SHUTDOWN_BUTTON_BOUNCE_TIME
        )
        