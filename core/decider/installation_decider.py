from core.scorecard_constants import *


def decide(visitor):

    final_score = (
        visitor["presence_score"] * AXIS_WEIGHT_PRESENCE +
        visitor["expression_score"] * AXIS_WEIGHT_EXPRESSION +
        visitor["context_score"] * AXIS_WEIGHT_CONTEXT +
        visitor["time_score"] * AXIS_WEIGHT_TIME
    )

    visitor["satisfaction_score"] = final_score
    visitor["output_type"] = "selphy"

    #rarity_unlocked_tier - filters to 3 types of rarity
    if final_score >= RARITY_RARE_MIN:
        visitor["unlocked_rarity_tier"] = ["rare" , "common" , "uncommon"]
    elif final_score >= RARITY_UNCOMMON_MIN:
        visitor["unlocked_rarity_tier"] = ["common" , "uncommon"]
    else:
        visitor["unlocked_rarity_tier"] = ["common"]
 
    print(f"[DECIDER] presence={visitor['presence_score']} expression={visitor['expression_score']} context={visitor['context_score']} time={visitor['time_score']}")
