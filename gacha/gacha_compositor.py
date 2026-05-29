

import numpy as np
from PIL import Image , ImageDraw , ImageChops
import random
from gacha.gacha_constants import *
import os

GOLDEN_ASSETS_DIR = "test/golden"


def get_golden():
    try :
        index = random.randint(1 ,5)
        filename=f"goldenspecial_{index}.jpg"
        golden_path = os.path.join(GOLDEN_ASSETS_DIR,filename)

        if not os.path.exists(golden_path):
            print(f"[GACHACOMPOSITOR] Golden Asset Not Found: {golden_path}")        
            return None
        
        return golden_path
    
    except Exception as e :
        print(f"[GACHACOMPOSITOR] Golden asset Error {e}")
        return None

def corrupt(filepath):

    image = Image.open(filepath)
    
    effects = [_chromatic_abberation, _glitch_shift, _ghost_print ,_pixel_band_sort, _scanlines,_invert_bands , _noise , _block_corrupt]
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

def _ghost_print(image):
    img_array = np.array(image).astype(np.float32)

    offset_x = random.randint(CHROMATIC_ABBERATION_OFFSET_MIN,CHROMATIC_ABBERATION_OFFSET_MAX)
    offset_y = random.randint(CHROMATIC_ABBERATION_OFFSET_MIN,CHROMATIC_ABBERATION_OFFSET_MAX)

    #two ghost copies shifted in different direction
    ghost1 = np.roll(img_array , offset_x ,axis = 1) #shift right
    ghost2 = np.roll(img_array , offset_y , axis = 0) #shift up

    #blend all three 
    result = (img_array * GHOST_PRINT_ORIGINAL_WEIGHT + ghost1 * GHOST_PRINT_GHOST_WEIGHT + ghost2 * GHOST_PRINT_GHOST_WEIGHT)
    result = np.clip(result , 0 , 255)

    return Image.fromarray(result.astype(np.uint8))

def _glitch_shift(image):
    img_array = np.array(image)

    height = img_array.shape[0]

    num_bands= random.randint(GLITCH_SHIFT_BANDS_MIN , GLITCH_SHIFT_BANDS_MAX)


    for _ in range(num_bands):
        y_start = random.randint(0 , height - GLITCH_BAND_HEIGHT_MAX)
        band_height = random.randint(GLITCH_BAND_HEIGHT_MIN , GLITCH_BAND_HEIGHT_MAX)

        y_end = min(y_start + band_height, height)

        shift = random.randint(GLITCH_SHIFT_AMOUNT_MIN , GLITCH_SHIFT_AMOUNT_MAX)

        direction = random.choice([1 , -1])

        img_array[y_start:y_end] = np.roll(img_array[y_start:y_end] , shift*direction, axis  =1)
        
        
    return Image.fromarray(img_array)
    


def _noise(image):
    img_array = np.array(image).astype(np.int16)


    noise = np.random.randint(-NOISE_INTENSITY , NOISE_INTENSITY , img_array.shape)
    result = np.clip(img_array + noise , 0 ,255)

    return Image.fromarray(result.astype(np.uint8))




def _block_corrupt(image):
    img_array = np.array(image)
    height, width = img_array.shape[:2]
    
    num_blocks = random.randint(BLOCK_CORRUPT_MIN, BLOCK_CORRUPT_MAX)
    
    for _ in range(num_blocks):
        x = random.randint(0, width - BLOCK_SIZE_MAX)
        y = random.randint(0, height - BLOCK_SIZE_MAX)
        w = random.randint(BLOCK_SIZE_MIN, BLOCK_SIZE_MAX)
        h = random.randint(BLOCK_SIZE_MIN, BLOCK_SIZE_MAX)
        
        mode = random.choice(["invert", "solid", "shift"])
        
        if mode == "invert":
            img_array[y:y+h, x:x+w] = 255 - img_array[y:y+h, x:x+w]
        elif mode == "solid":
            color = [random.randint(0, 255) for _ in range(3)]
            img_array[y:y+h, x:x+w] = color
        elif mode == "shift":
            img_array[y:y+h, x:x+w] = np.roll(img_array[y:y+h, x:x+w], random.randint(10, 50), axis=1)
    
    return Image.fromarray(img_array)

def _invert_bands(image):
    img_array = np.array(image)
    height = img_array.shape[0]
    
    num_bands = random.randint(INVERT_BANDS_MIN, INVERT_BANDS_MAX)
    
    for _ in range(num_bands):
        y_start = random.randint(0, height - INVERT_BAND_HEIGHT_MAX)
        band_height = random.randint(INVERT_BAND_HEIGHT_MIN, INVERT_BAND_HEIGHT_MAX)
        y_end = min(y_start + band_height, height)
        
        img_array[y_start:y_end] = 255 - img_array[y_start:y_end]
    
    return Image.fromarray(img_array)
