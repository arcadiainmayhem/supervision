from core.scorecard_constants import *


def decide(visitor):
    
    #SCORING



    base_score = (
        visitor["presence_score"] * BASE_W_PRESENCE + visitor["expression_score"] * BASE_W_EXPRESSION 
    )

    #CONTEXT + TIME MODIFIERS
    final_score = base_score * CONTEXT_MULT * TIME_MULT 

    visitor["satisfaction_score"] = final_score
    visitor["output_type"] = "selphy"



    #== PRESENCE GATE (item 6) — empty frame can't earn rare
    face = visitor["face_detected"]
    body = visitor["body_detected"]
    gated = (not face and not body)

    #== RARITY (item 5) — thresholds against real 0–1 base
    if not gated and final_score >= RARITY_RARE_MIN:
        visitor["unlocked_rarity_tier"] = ["common", "uncommon", "rare"]
    elif final_score >= RARITY_UNCOMMON_MIN:
        visitor["unlocked_rarity_tier"] = ["common", "uncommon"]
    else:
        visitor["unlocked_rarity_tier"] = ["common"]
 
    print(f"[DECIDER] base={base_score:.2f} final={final_score:.2f} "
        f"presence={visitor['presence_score']:.2f} expression={visitor['expression_score']:.2f} "
        f"tiers={visitor['unlocked_rarity_tier']}")
    