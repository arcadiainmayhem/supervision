from obelisk_compositor.obelisk_card_codex import *
from core.utils import weighted_pick



# def select(visitor):
#     rarity = visitor["rarity_tier"]

#     visitor["selected_elements"] = {
#         "background": weighted_pick(BACKGROUND_POOL[rarity]),
#         "border":     weighted_pick(BORDER_POOL[rarity]),
#         "face":       weighted_pick(FACE_POOL[rarity]),
#         "eye_1":      weighted_pick(EYE_POOL[rarity]),
#         "eye_2":      weighted_pick(EYE_POOL[rarity]),
#         "nose":       weighted_pick(NOSE_POOL[rarity]),
#         "mouth":      weighted_pick(MOUTH_POOL[rarity]),
#         "ear_1":      weighted_pick(EAR_POOL[rarity]),
#         "ear_2":      weighted_pick(EAR_POOL[rarity]),
#         "accessory":  weighted_pick(ACCESSORY_POOL[rarity]),
#         "detail":     weighted_pick(DETAIL_POOL[rarity]),   
#     }


    
def select(visitor):
    rarity = visitor["rarity_tier"]

    visitor["selected_elements"] = {
        "background" : weighted_pick(BACKGROUND_POOL[rarity]),
        "title" : weighted_pick(TITLE_POOL[rarity]),
        "border" : weighted_pick(BORDER_POOL[rarity]),
        "face":       weighted_pick(FACE_POOL[rarity]),
        "eyes":       weighted_pick(EYE_POOL[rarity]),
        "nose":       weighted_pick(NOSE_POOL[rarity]),
        "mouth":      weighted_pick(MOUTH_POOL[rarity]), 
        "logo" : weighted_pick(LOGO_POOL[rarity]),
    }


    