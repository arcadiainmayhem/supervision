

import json , os
from core.installation_constants import (
    PAPER_CAUTION_REMAINING,PAPER_PACK_MAX_CAPACITY ,
    INK_RIBBON_CAUTION_REMAINING,INK_RIBBON_MAX_CAPACITY,
    CONSUMABLES_STATE_PATH
)


_paper_used = 0
_ink_ribbon_used = 0



def load():
    global _paper_used , _ink_ribbon_used
    if os.path.exists(CONSUMABLES_STATE_PATH):
        try:
            with open(CONSUMABLES_STATE_PATH) as f:
                d = json.load(f)
                _paper_used = d.get("paper_used" , 0)
                _ink_ribbon_used = d.get("ink_ribbon_used", 0)
        except (json.JSONDecodeError, OSError) as e:
            print(f"[CONSUMABLES] Load Failed , starting at 0 : {e}")


def _save():
    try:
        with open(CONSUMABLES_STATE_PATH, "w") as f:
            json.dump({"paper_used" : _paper_used,
                       "ink_ribbon_used": _ink_ribbon_used}, f)
    except OSError as e:
        print(f"[CONSUMABLES] Save Failed : {e}")


def record_print():
    global _paper_used , _ink_ribbon_used

    _paper_used += 1
    _ink_ribbon_used += 1
    _save()


def _reset_paper():
    
    global _paper_used

    _paper_used = 0
    _save()


def _reset_ink_ribbon():
    
    global _ink_ribbon_used

    _ink_ribbon_used = 0
    _save()

def caution():
    paper_low = (PAPER_PACK_MAX_CAPACITY - _paper_used) <= PAPER_CAUTION_REMAINING
    ink_ribbon_low = ( INK_RIBBON_MAX_CAPACITY - _ink_ribbon_used) <= INK_RIBBON_CAUTION_REMAINING


    return paper_low or ink_ribbon_low

def get_counts():
    return {
        "paper_used" : _paper_used , "paper_cap" : PAPER_PACK_MAX_CAPACITY,
        "ink_ribbon_used" : _ink_ribbon_used , "ink_ribbon_cap" : INK_RIBBON_MAX_CAPACITY
    }