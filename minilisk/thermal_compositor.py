from PIL import Image, ImageDraw, ImageFont
from minilisk.thermal_slip_constants import *
from minilisk.thermal_slip_codex import IMAGE_KEYS
import textwrap

ASSETS_DIR = "test/Thermal_Trial_0905"

FONT_PATH = f"{ASSETS_DIR}/Fonts/Merchant_Copy.ttf"
FONT_LARGE = ImageFont.truetype(FONT_PATH, 72)
FONT_MEDIUM = ImageFont.truetype(FONT_PATH, 62)
FONT_SMALL = ImageFont.truetype(FONT_PATH, 40)

PADDING = 60
LINE_SPACING = 15

def compose_slip(assembled_data):
    canvas = Image.new('RGB', [THERMAL_SLIP_WIDTH, THERMAL_SLIP_HEIGHT], THERMAL_SLIP_BG_COLOR)
    draw = ImageDraw.Draw(canvas)
    y = THERMAL_SLIP_BORDER

    # title — full width, paste at left edge
    title = assembled_data.get("title")
    if title:
        try:
            img = Image.open(f"{ASSETS_DIR}/title/{title}").convert("RGBA")
            canvas.paste(img, (0, y), img)
            y += img.height + PADDING
        except FileNotFoundError:
            print(f"Missing title: {title}")

    # seal — centred
    seal = assembled_data.get("emblem_seal")
    if seal:
        try:
            img = Image.open(f"{ASSETS_DIR}/emblem_seal/{seal}").convert("RGBA")
            x = (THERMAL_SLIP_WIDTH - img.width) // 2
            canvas.paste(img, (x, y), img)
            y += img.height + PADDING
        except FileNotFoundError:
            print(f"Missing seal: {seal}")

    # readings
    for key in ["reading_1", "reading_2"]:
        value = assembled_data.get(key)
        if value:
            y = _draw_wrapped_text(draw, str(value), THERMAL_SLIP_BORDER, y, FONT_MEDIUM, THERMAL_SLIP_WIDTH)
            y += LINE_SPACING

    y += PADDING

    # small text row
    draw.text((THERMAL_SLIP_BORDER, y), str(assembled_data.get("lucky_number", "")), font=FONT_SMALL, fill="black")
    draw.text((THERMAL_SLIP_WIDTH // 2, y), str(assembled_data.get("moon_phase", "")), font=FONT_SMALL, fill="black")
    y += FONT_SMALL.size + LINE_SPACING
    draw.text((THERMAL_SLIP_BORDER, y), str(assembled_data.get("element", "")), font=FONT_SMALL, fill="black")
    y += FONT_SMALL.size + PADDING

    # footer
    draw.text((THERMAL_SLIP_BORDER, y), str(assembled_data.get("visitor_number", "")), font=FONT_SMALL, fill="black")
    y += FONT_SMALL.size + THERMAL_SLIP_BORDER

    # crop to actual content height
    canvas = canvas.crop((0, 0, THERMAL_SLIP_WIDTH, y))
    return canvas

def print_thermal_slip_escpos(assembled_data , printer):
    
    title = assembled_data.get("title")
    if title:
        try :
            img = Image.open(f"{ASSETS_DIR}/title/{title}").convert("L")
            print.img(img)
        except FileNotFoundError:
            print("Missing Title: {title}")

    seal = assembled_data.get("emblem_seal")
    if seal:
        try:
            img = Image.open()
            img = Image.open(f"{ASSETS_DIR}/emblem_seal/{seal}").convert("L")
            printer.set(align='center')
            printer.image(img)
        except FileNotFoundError:
            print(f"Missing seal: {seal}")

    #readings
    printer.set(align = 'left' , font = 'a' , double_height = True , double_width = False)
    printer.text(f"{assembled_data.get('reading_1', '')}\n\n")
    printer.text(f"{assembled_data.get('reading_2', '')}\n\n")

    # small text
    printer.set(align='left', font='a', double_height=False, double_width=False)
    printer.text(f"{assembled_data.get('lucky_number', '')}    {assembled_data.get('moon_phase', '')}\n")
    printer.text(f"{assembled_data.get('element', '')}\n\n")

    #footer
    printer.text(f"{assembled_data.get('visitor_number', '')}\n")

    print.cut ()


def _draw_wrapped_text(draw , text , x , y , font , max_width):
    #wrap at 35 characters
    lines = textwrap.wrap(text , width = 20)
    for line in lines:
        draw.text((x,y),line , font = font , fill = "black")
        y += font.size + LINE_SPACING
    return y




def print_thermal_slip_escpos(assembled, printer):
    #images
    title = assembled.get("title")
    if title:
        img = Image.open(f"{ASSETS_DIR}/title/{title}").convert("L")
        print.image(img)

    seal = assembled.get("emblem_seal")
    if seal:
        img = Image.open(f"{ASSETS_DIR}/emblem_seal/{seal}").convert("L")
        print.image(img)

    # native text
    printer.set(align='left', font='a', height=2, width=2)
    printer.text(f"{assembled.get('reading_1', '')}\n")
    printer.text(f"{assembled.get('reading_2', '')}\n")
    
    printer.set(align='left', font='a', height=1, width=1)
    printer.text(f"{assembled.get('lucky_number', '')}\n")
    printer.text(f"{assembled.get('moon_phase', '')}\n")
    printer.text(f"{assembled.get('element', '')}\n")
    printer.text(f"{assembled.get('visitor_number', '')}\n")
    
    printer.cut()