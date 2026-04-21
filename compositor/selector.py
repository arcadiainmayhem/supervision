from compositor.codex import *
from core.utils import weighted_pick


def select(categorised):

    #look at values via keys
    hue = categorised["hue_category"]
    brightness = categorised["brightness"]

    #get the right pools
    hue_elements = HUE_POOL[hue]
    brightness_elements = BRIGHTNESS_POOL[brightness]


    #pick one from each list
    selected = {
        "body" : weighted_pick(hue_elements["body"]),
        "head" :  weighted_pick(hue_elements["head"]),
        "limbs" :  weighted_pick(hue_elements["limbs"]),
        "detail" :  weighted_pick(brightness_elements["detail"]),
        "accessory" : weighted_pick(brightness_elements["accessory"]),
        "background" : weighted_pick(brightness_elements["background"]),
    }




    return selected