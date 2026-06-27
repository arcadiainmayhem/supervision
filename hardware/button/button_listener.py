

from hardware.hardware_config import *
from core.installation_constants import *
import time

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
        



# def register_shutdown_button(on_press):
#     if DEV_MODE:
#         print("Dev mode - press SPACE to trigger")
#         keyboard.add_hotkey('q',on_press)
#         print("Shutdown Button Ready")
#     else:
#         # GPIO.setmode(GPIO.BCM)

#         # GPIO.setup(SHUTDOWN_TRIGGER_PIN, GPIO.IN , pull_up_down= GPIO.PUD_UP)
#         # #Added to clear buffer
#         # GPIO.remove_event_detect(SHUTDOWN_TRIGGER_PIN)

#         # GPIO.add_event_detect(
#         #     SHUTDOWN_TRIGGER_PIN,
#         #     GPIO.FALLING,
#         #     callback= on_press,
#         #     bouncetime=SHUTDOWN_BUTTON_BOUNCE_TIME
#         # )
#         register_hold_button(SHUTDOWN_TRIGGER_PIN , on_press , SHUTDOWN_BUTTON_BOUNCE_TIME)


def register_hold_button( pin , callback , hold_duration = SHUTDOWN_HOLD_DURATION):

    if DEV_MODE:
        print(f"[BUTTONLISTENER] DEV Hold-Button Registered")
        return


    GPIO.setup(pin , GPIO.IN , pull_up_down=GPIO.PUD_UP) #internall pull up resistor holds the pin at 1 at rest 

    GPIO.remove_event_detect(pin)

    def _on_edge(channel):
        #press detected - confirm it stays hold

        start = time.time()
        while time.time() - start < hold_duration:
            if GPIO.input(pin) != GPIO.LOW: #HIGH -> LOW measures change
                print("[BUTTONLISTENER] Released too early - aborted")
                return
            time.sleep(HOLD_POLL_INTERVAL)

        #survived full window
        print("[BUTTONLISTENER] Hold Confirmed")
        callback()


    GPIO.add_event_detect(pin , GPIO.FALLING, callback=_on_edge, bouncetime= 300)