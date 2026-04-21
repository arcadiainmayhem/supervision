
from PIL import Image, ImageDraw
from compositor.constants import CARD_WIDTH , CARD_HEIGHT , CARD_BG_COLOR 
from compositor.constants import ELEMENT_POSITIONS
from compositor.shapes import draw_shapes


Z_ORDER = ["background" , "limbs" ,"body" , "head", "detail" , "accessory"]



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