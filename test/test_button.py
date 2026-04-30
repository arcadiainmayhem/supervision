import RPi.GPIO as GPIO
import time




GPIO.setmode(GPIO.BCM)
GPIO.setup(17 , GPIO.IN , pull_up_down=GPIO.PUD_UP)


print("Press the Button...")

while True:
    if GPIO.input(17) == GPIO.LOW:
        print("BUTTON IS BEING PRESSED")
    time.sleep(0.1)