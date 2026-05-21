

import numpy as np
from PIL import Image , ImageDraw , ImageChops
import random
from gacha.gacha_constants import *

def corrupt(filepath):

    image = Image.open(filepath)
    
    effects = [_chromatic_abberation, _pixel_band_sort, _scanlines, _vignette]
    #shuffle order
    random.shuffle(effects)

    #select up to 2 effects
    count = random.randint(2 , len(effects))
    #rearrange?
    selected = effects[:count]

    for effect in selected:
        print(f"[GACHAMANAGER] Effects Applied : {effect}")
        image = effect(image)


    #save corrupted
    corrupted_path = filepath.replace(".png" , "_corrupted.png")
    image.save(corrupted_path)


    return corrupted_path


def _chromatic_abberation(image):
    img_array = np.array(image)


    offset = random.randint(CHROMATIC_ABBERATION_OFFSET_MIN , CHROMATIC_ABBERATION_OFFSET_MAX)
    axis = random.choice ([0 , 1])

    r = img_array[: , : , 0].copy() #red
    g= img_array[:,:,1].copy() #green
    b= img_array[:,:,2].copy() #blue

    r = np.roll(r, offset , axis = axis) #shifts one way
    b = np.roll (b, -offset , axis = axis) #shifts opposit

    img_array[: , : , 0] = r
    img_array[: , : , 1] = g
    img_array[: , : , 2] = b


    return Image.fromarray(img_array)


def _pixel_sort(image):
    img_array = np.array(image)
    axis = random.choice([0,1])

    #sort by brightness
    brightness = img_array.mean(axis = 2)
    indices = np.argsort(brightness , axis = axis)

    #apply sort for each channel
    for c in range(3):
        img_array[ : , : , c] = np.take_along_axis(img_array[: , : , c], indices , axis=axis)


    return Image.fromarray(img_array)

def _scanlines(image):
    overlay = Image.new("RGBA",image.size, (0,0,0,0))
    draw = ImageDraw.Draw(overlay)

    spacing = random.randint(SCANLINES_SPACING_MIN,SCANLINES_SPACING_MAX)
    opacity = random.randint(SCANLINES_OPACITY_MIN , SCANLINES_OPACITY_MAX)

    for y in range(0 , image.size[1] , spacing):
        draw.line([(0,y) ,(image.size[0],y)], fill = (0,0,0,opacity))
                  
    return Image.alpha_composite(image.convert("RGBA"),overlay).convert("RGB")


def _vignette(image):
    width, height = image.size

    vignette = Image.new("L" , (width,height),0)

    for y in range (height):
        for x in range(width):

            #distance from center , normalised 0 - 1
            dx = (x - width/2 )/(width /2)
            dy = (y - height /2 )/ (height / 2)
            dist = min(1.0, (dx**2 + dy**2) ** 0.5)
            vignette.putpixel((x,y),int(dist * VIGNETTE_MULTI))


    image = image.convert("RGBA")
    r , g , b , a = image.split()

    r = ImageChops.subtract(r , vignette)
    g = ImageChops.subtract(g , vignette)
    b = ImageChops.subtract(b , vignette)


    return Image.merge("RGBA", (r, g, b, a)).convert("RGB")

def _pixel_band_sort(image):
    img_array = np.array(image)
    height = img_array.shape[0]
    
    # sort only random bands
    num_bands = random.randint(3, 8)
    for _ in range(num_bands):
        y_start = random.randint(0, height - 20)
        band_height = random.randint(5, 20)
        y_end = min(y_start + band_height, height)
        
        band = img_array[y_start:y_end, :, :]
        brightness = band.mean(axis=2)
        indices = np.argsort(brightness, axis=1)
        for c in range(3):
            band[:, :, c] = np.take_along_axis(band[:, :, c], indices, axis=1)
        img_array[y_start:y_end, :, :] = band
    
    return Image.fromarray(img_array)