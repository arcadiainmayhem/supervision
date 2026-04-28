


SYMBOLS = { 
    "warm" : "seal_fire.png",
    "cool" : "seal_water.png",
    "neutral" : "seal_earth.png",
}


def pick(visitor_data):
    return SYMBOLS.get(visitor_data["hue_category"] , "seal_default.png" )