
import os
from PIL import Image, ImageDraw
from obelisk_compositor.obelisk_card_constants import *
from obelisk_compositor.obelisk_card_constants import ELEMENT_POSITIONS_IAF , Z_ORDER_IAF
from core.placeholder_shapes import draw_shapes



def composite_elements(selected):
    
    #create new canvas
    canvas = Image.new("RGBA",[CARD_WIDTH , CARD_HEIGHT] , CARD_BG_COLOR)
    #draw on created canvas
    draw = ImageDraw.Draw(canvas)


    for layer in Z_ORDER_IAF:
        filename = selected.get(layer)
        #skip gracefully
        if filename is None:
            continue
        position = ELEMENT_POSITIONS_IAF[layer]
        path = f"{ASSETS_DIR}/{layer}/{filename}"
        
        #error handling
        try:
            img = Image.open(path).convert("RGBA")
            
            #print(img.getbbox())

            canvas.paste(img, position ,img)

        except FileNotFoundError:
            print(f"Missing asset: {path} - skipping layer {layer}")
        except Exception as e:
            print (f"Layer {layer} failed : {e} - skipping")
            
    return canvas.convert("RGB")