
from core.generators.reading_generator import pick as pick_readings
from core.generators.symbol_generator import pick as pick_symbol
from core.generators.number_generator import calculate as calculate_number
from core.generators.context_reader import get_context
from minilisk.thermal_slip_codex import *
from minilisk.thermal_slip_constants import *
import random
import os

def _verify_exists( picked_filename , availble_filenames, subfolder):
    path = os.path.join(THERMAL_ASSETS_DIR , subfolder , picked_filename)

    if os.path.exists(path):
        return picked_filename
    

    print(f"[THERMAL ASSEMBLER] MISSING: {path} - resampling from pool")

    others = [f for f in availble_filenames if f != picked_filename]
    random.shuffle(others)


    for candidate in others:
        candidate_path = os.path.join(THERMAL_ASSETS_DIR, subfolder , candidate)
        if os.path.exists(candidate_path):
            return candidate
        

    print(f"[THERMAL ASSEMBLER] Warning: Entire Pool Missing for '{subfolder} - skipping layer")
    return None

def assemble(visitor):

    picked_title = random.choice(TITLE_POOL)

    picked_seal = pick_symbol(visitor)

    element = visitor.get("element" , "earth")
    seal_pool = EMBLEM_SEAL_POOL.get(element , EMBLEM_SEAL_POOL["earth"])



    return {
        "title":        _verify_exists(picked_title, TITLE_POOL, "title"),
        "subtitle":     "Prima Materia",
        "emblem_seal":  _verify_exists(picked_seal, seal_pool, "emblem_seal"),
        "reading_1":    pick_readings(visitor),
        "reading_2":    pick_readings(visitor),
        "lucky_number": f"Lucky Number: {visitor['numerology']}",
        "moon_phase":   f"Moon: {visitor['moon_phase']}",
        "element":      f"Element Affinity: {visitor['element']}",
        "Footer_1":     visitor["visitor_number"],
    }