


STATE_COLORS = {
    "idle":       (0, 50, 50),    # dim cyan pulse
    "triggered":  (255, 255, 0),  # yellow flash
    "processing": (0, 0, 255),    # blue shift
    "printing":   (0, 255, 0),    # green steady
    "completed":  (255, 255, 255),# white
    "error":      (255, 0, 0),    # red
    "bored":      (128, 0, 128),  # purple
    "proud":      (255, 100, 0),  # orange
    "gacha" :  (255,160,0), #golden yellow?
    "satan" : None #animated - handled by manager , white yellow red
}

LED_CHANNEL = 1

FLASH_TIMES = 4
CHASE_SPEED = 0.1
FADE_SPEED = 0.02
SLEEP_TIME = 0.1