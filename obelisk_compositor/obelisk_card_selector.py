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
    unlocked = visitor["unlocked_rarity_tier"]
    selected = {}
      
    slots = {
        "background" : BACKGROUND_POOL,
        "title" : TITLE_POOL,
        "border" : BORDER_POOL,
        "face":       FACE_POOL,
        "eyes":       EYE_POOL,
        "nose":       NOSE_POOL,
        "mouth":      MOUTH_POOL, 
        "logo" : LOGO_POOL,
    }

    #looks through and verify the filename exists
    for layer, pool in slots.items():
        combined = []
        for tier in unlocked:
            if tier in pool:
                combined.extend(pool[tier])
        picked_filename = weighted_pick(combined)
        selected[layer] = _verify_exists(picked_filename, combined, layer)

    visitor["selected_elements"] = selected
    