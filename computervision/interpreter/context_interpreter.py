from core.scorecard_constants import *



def intepret_context (visitor):

    context_score = 0

    current_moon_phase =   visitor["moon_phase"] 
    current_element  = visitor["element"]
    current_numerology_number = visitor["numerology"] 

    print("Numerology value:", current_numerology_number)
    print("Element:", current_element)
    print("Current Moon Phase:", current_moon_phase)

    #MOON MEANING

    if current_moon_phase == "waning":
        context_score += SCORE_MOON_WANING
    elif current_moon_phase == "waxing":
        context_score += SCORE_MOON_WAXING
    elif current_moon_phase == "full":
        context_score += SCORE_MOON_FULL
    elif current_moon_phase == "new":
        context_score += SCORE_MOON_NEW
    else:
        context_score += SCORE_MOON_NEW


    #ELEMENT MEANING
    if current_element == "fire":
        context_score += SCORE_SIGIL_ELEMENT_FIRE
    elif current_element == "water":
        context_score += SCORE_SIGIL_ELEMENT_WATER
    elif current_element == "air":
        context_score += SCORE_SIGIL_ELEMENT_AIR
    elif current_element == "earth":
        context_score += SCORE_SIGIL_ELEMENT_EARTH
    elif current_element == "unknown":
        context_score += SCORE_SIGIL_ELEMENT_UNKNOWN

    #NUMERLOGY NUMBER MEANING
    if current_numerology_number is None:
        context_score += SCORE_NUMEROLOGY_ELSE
    elif current_numerology_number == 0:
        context_score += SCORE_NUMEROLOGY_0
    elif current_numerology_number == 1:
        context_score += SCORE_NUMEROLOGY_1
    elif current_numerology_number == 7:
        context_score += SCORE_NUMEROLOGY_7
    elif current_numerology_number % 2 == 0:   # even — remainder is 0
        context_score += SCORE_NUMEROLOGY_EVEN
    else:                                        # odd
        context_score += SCORE_NUMEROLOGY_ODD

    if current_moon_phase == "full" and current_element in("fire" ,  "earth"):
        label = ContextLabel.COAGULATION
    elif current_moon_phase == "full" and current_element in ("water" ,  "air" ):
        label = ContextLabel.MYSTERIOUS
    elif current_moon_phase == "new":
        label = ContextLabel.LIMINAL
    elif current_moon_phase == "waning" and current_element == "water":
        label = ContextLabel.DISSOLUTION
    elif current_element == "unknown":
        label = ContextLabel.MYSTERIOUS
    else:
        label= ContextLabel.NEUTRAL


    visitor["context_score"] = context_score
    visitor["context_label"] = label

