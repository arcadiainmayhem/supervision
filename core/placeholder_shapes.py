from PIL import ImageDraw
import random

def random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def draw_shapes(draw, layer, position):
    if layer == "mouth":
        draw.arc(position, start=0, end=180, fill=random_color(), width=3)
    elif layer == "border":
        draw.rectangle(position, fill=None, outline=random_color(), width=3)
    else:
        draw.ellipse(position, fill=random_color())

def draw_placeholder(draw, position, label):
    x, y = position
    draw.rectangle([x, y, x + 200, y + 30], fill=random_color(), outline='black', width=1)
    draw.text((x + 5, y + 5), label, fill='black')