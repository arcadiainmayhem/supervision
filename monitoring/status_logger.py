
from datetime import datetime

encounter_log = [] #encounter history
error_log = [] #errors only


current_status = {
    "printer" : "unknown",
    "camera": "unknown",
    "state" : "idle",
    "triggers_today" : 0,

}



def log_encounter(visitor):
    entry = {
        "visitor_number" : visitor["visitor_number"],
        "timestamp" : visitor["timestamp"].strftime("%H:%M"),
        "rarity" : visitor["rarity_tier"],
        "score" : round(visitor["satisfaction_score"] , 2),
        "printed":visitor.get("printed",False)
    }
    encounter_log.append(entry)
    #logs and increases count
    current_status["triggers_today"] += 1



def log_error(source,message):
    entry = {
        "time" : datetime.now().strftime("%H:%M:%S"),
        "source" : source,
        "message" : message,
    }

    error_log.append(entry)
    print(f"[ERROR] {source} : {message}")


def update_status(key , value):
    current_status[key] = value