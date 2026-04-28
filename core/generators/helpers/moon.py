

import ephem
from datetime import datetime





PHASE_CATEGORIES = {
    "new" : ... ,
    "waxing" : ... ,
    "full" : ...,
    "waning" : ... 
}


def _categorise(phase):
    if phase < 10: return "new"
    elif phase < 45: return "waxing"
    elif phase < 55 : return "full"
    elif phase < 90 : return "waning"
    else:
        return "new"

def get_phase_of_moon():
    moon = ephem.Moon()
    moon.compute(datetime.now())
    phase = moon.phase #illumination %
    return _categorise(phase)