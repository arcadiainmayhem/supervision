

from PIL import Image, ImageDraw

import random

def draw_shapes(draw , layer , position):
    if layer == "body":
        draw_body(draw,position)
    elif layer == "background":
        draw_background(draw,position)
    elif layer == "head":
        draw_head(draw,position)
    elif layer == "detail":
        draw_detail(draw,position)
    elif layer == "accessory":
        draw_accessory(draw,position)
    elif layer == "limbs":
        draw_limbs(draw,position)


def random_color():
    return (random.randint(0,255),random.randint(0,255),random.randint(0,255))

def draw_head(draw , position):
    draw.ellipse(position, fill=random_color(), outline=None, width=1)
    
def draw_body(draw,position):
    draw.rectangle(position, fill= random_color(), outline=None, width=1)

def draw_limbs(draw,position):
    draw.ellipse(position, fill= random_color(), outline=None, width=1)

def draw_detail(draw,position):
    draw.rectangle(position, fill= random_color(), outline=None, width=1)

def draw_accessory(draw,position):
    draw.ellipse(position, fill= random_color(), outline=None, width=1)


def draw_background(draw,position):
    draw.rectangle(position, fill= random_color(), outline=None, width=1)


def draw_placeholder(draw , position , label):
    x , y = position
    draw.rectangle([x, y , x + 200 , y + 30], fill= random_color(), outline='black', width=1)
    draw.text((x+5,y+5),label , fill='black' )