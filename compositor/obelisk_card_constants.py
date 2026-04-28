



#CARD RELATED
CARD_WIDTH = 500
CARD_HEIGHT = 700
CARD_BG_COLOR = 'white'


#COMPOSITOR RELATED
ELEMENT_POSITIONS = {
    "background": (0, 0, CARD_WIDTH, CARD_HEIGHT),
    "body":       (CARD_WIDTH * 0.35, CARD_HEIGHT * 0.43, CARD_WIDTH * 0.65, CARD_HEIGHT * 0.83),
    "head":       (CARD_WIDTH * 0.35, CARD_HEIGHT * 0.14, CARD_WIDTH * 0.65, CARD_HEIGHT * 0.40),
    "limbs":      (CARD_WIDTH * 0.20, CARD_HEIGHT * 0.46, CARD_WIDTH * 0.80, CARD_HEIGHT * 0.74),
    "detail":     (CARD_WIDTH * 0.40, CARD_HEIGHT * 0.21, CARD_WIDTH * 0.60, CARD_HEIGHT * 0.34),
    "accessory":  (CARD_WIDTH * 0.60, CARD_HEIGHT * 0.11, CARD_WIDTH * 0.80, CARD_HEIGHT * 0.26),
}


Z_ORDER = ["background" , "limbs" ,"body" , "head", "detail" , "accessory"]
