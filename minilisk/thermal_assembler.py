
from core.generators.reading_generator import pick as pick_readings
from core.generators.symbol_generator import pick as pick_symbol
from core.generators.number_generator import calculate as calculate_number
from core.generators.context_reader import get_context

def assemble(visitor):
    return {
        "title": None,
        "subtitle": None,
        "emblem_seal": pick_symbol(visitor),
        "reading_1": pick_readings(visitor),
        "reading_2": pick_readings(visitor),
        "reading_3": pick_readings(visitor),
        "reading_4": pick_readings(visitor),
        "lucky_number": visitor["numerology"],
        "moon_phase": visitor["moon_phase"],
        "element": visitor["element"],
        "Footer_1": visitor["visitor_number"],
        "Footer_2": None,
        "datestamp": visitor["datestamp"],
        "dwell_time": (visitor["end_time"] - visitor["start_time"]).seconds if visitor["end_time"] else 0,
    }