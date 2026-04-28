
from PIL import Image, ImageDraw
from compositor.obelisk_card_constants import CARD_WIDTH , CARD_HEIGHT , CARD_BG_COLOR 
from compositor.obelisk_card_constants import ELEMENT_POSITIONS , Z_ORDER
from core.placeholder_shapes import draw_shapes





def composite_elements(selected):
    
    #create new canvas
    canvas = Image.new("RGB",[CARD_WIDTH , CARD_HEIGHT] , CARD_BG_COLOR)
    #draw on created canvas
    draw = ImageDraw.Draw(canvas)


    for layer in Z_ORDER:
        element = selected.get(layer)
        if element is None:
            continue
        position = ELEMENT_POSITIONS[layer]

        draw_shapes(draw , layer , position)

    return canvas