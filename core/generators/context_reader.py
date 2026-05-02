
from core.generators.helpers.astrology import get_element
from core.generators.helpers.moon import get_phase_of_moon
from core.generators.helpers.numerology import calculate


def get_context(visitor):
    visitor["moon_phase"] = get_phase_of_moon()   
    visitor["element"] = get_element(visitor["datestamp"])
    visitor["numerology"] = calculate(visitor)



   