
from core.generators.helpers.astrology import get_sun_sign
from core.generators.helpers.moon import get_phase_of_moon
from core.generators.helpers.numerology import calculate


def get_context(visitor_data):
    print("returning context dictionary")
    print("getting moon...")
    moon = get_phase_of_moon()
    print("getting element...")
    sun_sign = get_sun_sign(visitor_data["datestamp"])
    print("getting numerology...")
    numerology = calculate(visitor_data)
    print("returning context...")
    return {
        "moon_phase" : moon,
        "element" : sun_sign,
        "numerology" : numerology
    }