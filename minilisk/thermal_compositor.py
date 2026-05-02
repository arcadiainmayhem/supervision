
from PIL import Image , ImageDraw
from minilisk.thermal_slip_constants import *
from core.placeholder_shapes import *


def compose_slip(assembled_data):
    #create canvas

    canvas = Image.new('RGB' , [THERMAL_SLIP_WIDTH , THERMAL_SLIP_HEIGHT] , THERMAL_SLIP_BG_COLOR )
    
    #draw on created canvas
    draw = ImageDraw.Draw(canvas)

    #loop through elements + draw + return
    for key in SLIP_LAYOUT:
        position = SLIP_LAYOUT[key]
        value = assembled_data.get(key , "missing") #fallback is missing
        #print(f"{key} : {position}")
        draw_placeholder(draw , position , f"{key}: {value}")

    # canvas.show()
    return canvas