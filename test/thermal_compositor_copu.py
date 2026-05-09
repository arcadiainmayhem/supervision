
from PIL import Image , ImageDraw , ImageFont
from minilisk.thermal_slip_constants import *
from core.placeholder_shapes import *
from minilisk.thermal_slip_codex import *

ASSETS_DIR = "test/Thermal_Trial_0905"

FONT_PATH = "C:/Windows/Fonts/cour.ttf"
FONT_LARGE = ImageFont.truetype(FONT_PATH, 40)
FONT_MEDIUM = ImageFont.truetype(FONT_PATH, 28)
FONT_SMALL = ImageFont.truetype(FONT_PATH, 20)

def compose_slip(assembled_data):
    #create canvas

    canvas = Image.new('RGB' , [THERMAL_SLIP_WIDTH , THERMAL_SLIP_HEIGHT] , THERMAL_SLIP_BG_COLOR )
    
    #draw on created canvas
    draw = ImageDraw.Draw(canvas)

    # #loop through elements + draw + return
    # for key in SLIP_LAYOUT:
    #     position = SLIP_LAYOUT[key]
    #     value = assembled_data.get(key , "missing") #fallback is missing
    #     #print(f"{key} : {position}")
    #     draw_placeholder(draw , position , f"{key}: {value}")

    _draw_image(canvas , assembled_data)
    _draw_text(draw , assembled_data)

    # canvas.show()
    return canvas

def _draw_text( draw, assembled_data):
    for key in SLIP_LAYOUT:
        if key in IMAGE_KEYS:
            continue
        value= assembled_data.get(key , None)
        if value is None:
            continue
        position = SLIP_LAYOUT[key]
        draw.text(position , str(value), font = FONT_SMALL , fill = "black")


def _draw_image(canvas , assembled_data):
    for key in SLIP_LAYOUT:
        if key in IMAGE_KEYS:
            value = assembled_data.get(key , None)
            if value is None:
                continue
            path = f"{ASSETS_DIR}/{key}/{value}"
            try:
                img = Image.open(path).convert("RGBA")
                #get position from sliplayout in constants
                position = SLIP_LAYOUT[key]
                canvas.paste ( img , position , img)
            except FileNotFoundError:
                print(f"Missing thermal asset: { path} - skipping")
            

def _draw_decorative_border(canvas):
    #TODO
    pass