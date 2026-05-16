from obelisk_compositor.obelisk_card_codex import *
from obelisk_compositor.obelisk_card_constants import *

from core.utils import weighted_pick
import os
import random

    
def _verify_exists(picked_filename, available_filenames, layer):
    path = os.path.join(ASSETS_DIR, layer, picked_filename)

    if os.path.exists(path):
        return picked_filename

    print(f"[SELECTOR] Missing: {path} — resampling from pool")

    others = [f for f in available_filenames if f != picked_filename]
    random.shuffle(others)

    for candidate in others:
        candidate_path = os.path.join(ASSETS_DIR, layer, candidate)
        if os.path.exists(candidate_path):
            return candidate

    print(f"[SELECTOR] WARNING: entire pool missing for layer '{layer}' — skipping")
    return None


def select(visitor):
    rarity = visitor["rarity_tier"]
    selected = {}
      
    slots = {
        "background" : BACKGROUND_POOL[rarity],
        "title" : TITLE_POOL[rarity],
        "border" : BORDER_POOL[rarity],
        "face":       FACE_POOL[rarity],
        "eyes":       EYE_POOL[rarity],
        "nose":       NOSE_POOL[rarity],
        "mouth":      MOUTH_POOL[rarity], 
        "logo" : LOGO_POOL[rarity],
    }

    #looks through and verify the filename exists
    for layer, available_filenames in slots.items():
        picked_filename = weighted_pick(available_filenames)
        selected[layer] = _verify_exists(picked_filename, available_filenames, layer)

    visitor["selected_elements"] = selected
    