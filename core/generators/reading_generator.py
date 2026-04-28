

import random

#HUE CATEGORY
WARM_READINGS = [
    "warm_reading_a",
    "warm_reading_b",
    "warm_reading_c",

]

COOL_READINGS = [
    "cool_reading_a",
    "cool_reading_b",
    "cool_reading_c",
    
]

NEUTRAL_READINGS = [
    "neutral_reading_a",
    "neutral_reading_b",
    "neutral_reading_c",

]

def pick(visitor_data):

    if visitor_data["hue_category"] == "warm":
        return random.choice(WARM_READINGS)
    elif visitor_data["hue_category"] == "cool":
        return random.choice(COOL_READINGS)
    elif visitor_data["hue_category"] == "neutral":
        return random.choice(NEUTRAL_READINGS)
