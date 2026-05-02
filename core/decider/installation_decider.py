from core.scorecard_constants import *


def decide(visitor):

    final_score = (
        visitor["presence_score"] * AXIS_WEIGHT_PRESENCE +
        visitor["expression_score"] * AXIS_WEIGHT_EXPRESSION +
        visitor["context_score"] * AXIS_WEIGHT_CONTEXT +
        visitor["time_score"] * AXIS_WEIGHT_TIME
    )

    visitor["satisfaction_score"] = final_score

    #rarity_tier - filters to 3 types of rarity
    if final_score >= RARITY_RARE_MIN:
        visitor["rarity_tier"] = "rare"
    elif final_score >= RARITY_UNCOMMON_MIN:
        visitor["rarity_tier"] = "uncommon"
    else:
        visitor["rarity_tier"] = "common"

    # output type
    if final_score >= OUTPUT_SELPHY_THRESHOLD:
        visitor["output_type"] = "selphy"
    else:
        visitor["output_type"] = "thermal"
