
from core.generators.reading_generator import pick as pick_readings
from core.generators.symbol_generator import pick as pick_symbol
from core.generators.number_generator import calculate as calculate_number
from core.generators.context_reader import get_context
from minilisk.thermal_slip_codex import *
import random

def assemble(visitor):
    return {
        "title": random.choice(TITLE_POOL),
        "subtitle": "Prima Materia",
        "emblem_seal": pick_symbol(visitor),
        "reading_1": pick_readings(visitor),
        "reading_2": pick_readings(visitor),
        "lucky_number": f"Lucky Number: {visitor["numerology"]}",
        "moon_phase": f"Moon: { visitor["moon_phase"]}",
        "element": f"Element Affinity: {visitor["element"]}",
        "Footer_1": visitor["visitor_number"],

    }