
from datetime import datetime
from core.scorecard_constants import *

def intepret_time(visitor):

    hour = visitor["timestamp"].hour


    if 4 <= hour <= 10:
        label = TimeLabel.MORNING
        time_score = SCORE_TIME_MORNING
    elif 11 <= hour <= 15:
        label = TimeLabel.EARLYAFTERNOON
        time_score = SCORE_TIME_EARLYAFTERNOON
    elif 16 <= hour <= 18:
        label = TimeLabel.LATEAFTERNOON
        time_score = SCORE_TIME_LATEAFTERNOON
    elif 19 <= hour <= 22:
        label = TimeLabel.EVENING
        time_score = SCORE_TIME_EVENING
    else:  # 23 - 4
        label = TimeLabel.DEEPOFNIGHT
        time_score = SCORE_TIME_DEEPOFNIGHT


    visitor["time_score"] = time_score
    visitor["time_label"] = label