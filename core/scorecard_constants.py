
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
    

    

#--PRESENCE AXIS
SCORE_FACE_DETECTED = 0.10 #COMMON

# ── FACE ORIENTATION SCORES ────────────────────
SCORE_FACE_FRONT          = 0.12
SCORE_FACE_DOWN           = 0.22   # bowed — deferential
SCORE_FACE_LEFT           = 0.15
SCORE_FACE_RIGHT          = 0.15
SCORE_FACE_UP             = 0.08   # disengaged

SCORE_BODY_DETECTED = 0.1 # COMMON 

SCORE_PERSON_SOLO = 0.1
SCORE_MULTI_PERSON_2_4 = -0.2 #UNSURE WHICH SUBJECT IT IS , AMBIGUOUS
SCORE_MULTI_PERSON_5_PLUS = 0.2 #RARE -TODO MIGHT NEED TO GUARD AGAINST CROWD RECOGNITION AND FACTORING THAT IN


#--EXPRESSION AXIS
SCORE_HUE_WARM = 0.12
SCORE_HUE_COOL = 0.13
SCORE_HUE_NEUTRAL = 0.09
SCORE_BRIGHTNESS_LIGHT = 0.13
SCORE_BRIGHTNESS_DARK = 0.12
SCORE_BRIGHTNESS_MEDIUM = 0.12

#GESTURES
SCORE_GESTURE_PRAYING = 0.25  # rare, intentional
SCORE_GESTURE_OPEN_PALM   = 0.10   # receptive
SCORE_GESTURE_CLOSED_FIST = -0.20
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
AXIS_WEIGHT_PRESENCE = 0.50
AXIS_WEIGHT_EXPRESSION = 0.40
AXIS_WEIGHT_CONTEXT = 0.35
AXIS_WEIGHT_TIME = 0.10

#--OUTPUT THRESHOLD
OUTPUT_SELPHY_THRESHOLD = 0.75


#--RARITY TIERS
RARITY_RARE_MIN           = 0.85
RARITY_UNCOMMON_MIN       = 0.65