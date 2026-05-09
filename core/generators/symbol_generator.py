import random
from minilisk.thermal_slip_codex import *


def pick(visitor_data):
    element = visitor_data.get("element" , "earth")
    pool = EMBLEM_SEAL_POOL.get(element , EMBLEM_SEAL_POOL["earth"])
    return random.choice(pool)