
from enum import Enum

class PresenceLabel(Enum):
    ABSENT = "absent" #no body or no face
    PARTIAL = "partial" #body only , no face / face only , no body
    PRESENT = "present" #face detected, face forward
    AVERTED = "averted" #face detected, face orientation != forward
    DEFERENTIAL = "deferential" #face down
    CROWD = "crowd" #5+ people

class ExpressionLabel(Enum):
    WARM_LIGHT = "warm_light"
    WARM_DARK = "warm_dark"
    COOL_LIGHT = "cool_light"
    COOL_DARK = "cool_dark"
    NEUTRAL = "neutral"
    EXPRESSIVE = "expressive"


class ContextLabel(Enum):
    COAGULATION   = "coagulation"   # full moon , things solidifying
    LIMINAL      = "liminal"      # new moon, threshold moments
    NEUTRAL      = "neutral"
    DISSOLUTION    = "dissolution"       # diminishing / waning / breaking down
    MYSTERIOUS = "mysterious"  # air + water - unknowable and shifting

class TimeLabel(Enum):
    MORNING = "morning"
    EARLYAFTERNOON = "early_afternoon"
    LATEAFTERNOON = "late_afternoon"
    EVENING = "evening"
    DEEPOFNIGHT = "deep_of_night"
    


#NORMALISED PRESENCE ( WEIGHING TO 1 )
PRESENCE_W_FACE = 0.45
PRESENCE_W_BODY = 0.20
PRESENCE_W_COUNT = 0.25
PRESENCE_W_STILLNESS = 0.1

FACE_ORIENTATION_DIRECTION = {
    "forward" : 1.0 ,
    "down" : 0.7, 
    "left" : 0.6,
    "right" : 0.6,
    "up" : 0.3, #disengaged
    "unknown" : 0.1
}

#PERSON COUNT
PERSON_COUNT_SOLO = 1.0 #one clear subject
PERSON_COUNT_PAIR = 0.3 #2 - 4
PERSON_COUNT_CROWD = 0.5 #>0.5
PERSON_COUNT_NONE = 0.0


#--EXPRESSION AXIS
EXPRESSION_W_COLOR = 0.4
EXPRESSION_W_GESTURE = 0.6


HUE_QUALITY = {
    "cool" : 1.0,
    "warm" : 0.9,
    "neutral" : 0.55
}

BRIGHTNESS_QUALITY = {
    "light" : 1.0,
    "dark" : 0.9,
    "medium" : 0.59,
}

SATURATION_QUALITY = {
    "muted" : 0.4,
    "moderate" : 0.67,
    "vivid" : 1.0
}

EXPRESSION_GESTURES = {
    "ILoveYou":    1.0,
    "Victory":     0.95,
    "Thumbs_Up":   0.70,
    "Open_Palm":   0.60,
    "Pointing_Up": 0.50,
    "Thumbs_Down": 0.50,
    "Closed_Fist": 0.10,
    "Praying" : 0.82,
    "Unknown":    0.12,
}

#GESTURES
SCORE_GESTURE_PRAYING = 0.25  # rare, intentional
SCORE_GESTURE_OPEN_PALM   = 0.10   # receptive
SCORE_GESTURE_CLOSED_FIST = 0.10
SCORE_GESTURE_POINTING_UP    = 0.05   # engaged but neutral
SCORE_GESTURE_THUMBS_DOWN = 0.08
SCORE_GESTURE_THUMBS_UP = 0.15
SCORE_GESTURE_VICTORY = 0.28
SCORE_GESTURE_LOVE = 0.30
SCORE_GESTURE_UNKNOWN = 0.00



#--CONTEXT AXIS 

SCORE_MOON_FULL = 0.20
SCORE_MOON_NEW = 0.15
SCORE_MOON_WANING = 0.10
SCORE_MOON_WAXING = 0.08

SCORE_SIGIL_ELEMENT_FIRE = 0.12
SCORE_SIGIL_ELEMENT_WATER = 0.09
SCORE_SIGIL_ELEMENT_EARTH = 0.10
SCORE_SIGIL_ELEMENT_AIR = 0.11
SCORE_SIGIL_ELEMENT_UNKNOWN = -0.20

#TO BE FILLED
SCORE_NUMEROLOGY_EVEN = 0.18
SCORE_NUMEROLOGY_ODD = 0.15
SCORE_NUMEROLOGY_7 = 0.07
SCORE_NUMEROLOGY_0 = 0.00
SCORE_NUMEROLOGY_1 = 0.11
SCORE_NUMEROLOGY_ELSE = -0.15

#--TIME AXIS
SCORE_TIME_MORNING = -0.15
SCORE_TIME_EARLYAFTERNOON = 0.12
SCORE_TIME_LATEAFTERNOON = 0.15
SCORE_TIME_EVENING = 0.20
SCORE_TIME_DEEPOFNIGHT = 0.24


#AXIS WEIGHTS IN FINAL SCORE
AXIS_WEIGHT_PRESENCE = 0.45
AXIS_WEIGHT_EXPRESSION = 0.35
AXIS_WEIGHT_CONTEXT = 0.15
AXIS_WEIGHT_TIME = 0.05

#BASE WEIGHTS IN FINAL SCORING
BASE_W_PRESENCE = 0.6
BASE_W_EXPRESSION = 0.4

CONTEXT_MULT = 1.0
TIME_MULT = 1.0


#--RARITY TIERS
RARITY_RARE_MIN           = 0.75
RARITY_UNCOMMON_MIN       = 0.58