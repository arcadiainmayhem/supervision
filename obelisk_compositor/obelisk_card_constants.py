



#CARD RELATED
CARD_WIDTH = 1200
CARD_HEIGHT = 1800
CARD_BG_COLOR = 'white'


#COMPOSITOR RELATED
ELEMENT_POSITIONS = {
    "background": (0, 0, CARD_WIDTH, CARD_HEIGHT),
    "border":     (0, 0, CARD_WIDTH, CARD_HEIGHT),
    "face":       (int(CARD_WIDTH * 0.25), int(CARD_HEIGHT * 0.15), int(CARD_WIDTH * 0.75), int(CARD_HEIGHT * 0.75)),
    "eye_1":      (int(CARD_WIDTH * 0.30), int(CARD_HEIGHT * 0.30), int(CARD_WIDTH * 0.47), int(CARD_HEIGHT * 0.42)),
    "eye_2":      (int(CARD_WIDTH * 0.53), int(CARD_HEIGHT * 0.30), int(CARD_WIDTH * 0.70), int(CARD_HEIGHT * 0.42)),
    "nose":       (int(CARD_WIDTH * 0.40), int(CARD_HEIGHT * 0.44), int(CARD_WIDTH * 0.60), int(CARD_HEIGHT * 0.56)),
    "mouth":      (int(CARD_WIDTH * 0.33), int(CARD_HEIGHT * 0.58), int(CARD_WIDTH * 0.67), int(CARD_HEIGHT * 0.68)),
    "ear_1":      (int(CARD_WIDTH * 0.10), int(CARD_HEIGHT * 0.30), int(CARD_WIDTH * 0.25), int(CARD_HEIGHT * 0.50)),
    "ear_2":      (int(CARD_WIDTH * 0.75), int(CARD_HEIGHT * 0.30), int(CARD_WIDTH * 0.90), int(CARD_HEIGHT * 0.50)),
    "detail":     (int(CARD_WIDTH * 0.35), int(CARD_HEIGHT * 0.20), int(CARD_WIDTH * 0.65), int(CARD_HEIGHT * 0.32)),
    "accessory":  (int(CARD_WIDTH * 0.60), int(CARD_HEIGHT * 0.10), int(CARD_WIDTH * 0.80), int(CARD_HEIGHT * 0.25)),
}

#COMPOSITOR RELATED
ELEMENT_POSITIONS_IAF = {
    "face":       (0 , 0),
    "eyes":       (0 , 0),
    "nose":        (0 , 0),
    "mouth":       (0 , 0),
}




#Z_ORDER = ["background" , "border" , "face" , "eye_1" ,"eye_2" , "nose", "ear_1" , "ear_2" , "mouth", "detail" , "accessory"]
 
Z_ORDER_IAF = [ "face" , "eyes" , "nose", "mouth"]
