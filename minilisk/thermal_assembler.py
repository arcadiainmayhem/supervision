
from core.generators.reading_generator import pick as pick_readings
from core.generators.symbol_generator import pick as pick_symbol
from core.generators.number_generator import calculate as calculate_number
from core.generators.context_reader import get_context

def assemble ( visitor , decider_output):
   print("assembling visitor data")
   visitor_data = _assemble_visitor_data(visitor)
   print("assembling decider data")
   decider_data = _assemble_decider_data(decider_output)
   print("getting context")
   context = get_context(visitor_data)
   print("building dictionary..")
   return {
        "title" : None,
        "subtitle": None,
        "emblem_seal": pick_symbol(visitor_data),
        "reading_1" : pick_readings(visitor_data),
        "reading_2" : pick_readings(visitor_data),
        "reading_3" : pick_readings(visitor_data),
        "reading_4" : pick_readings(visitor_data),
        #Esoteric Readings
        "lucky_number" : context["numerology"],
        "Moon Phase" : context["moon_phase"],
        "Element_Affinity": context["element"],
        "Footer_1" : visitor_data["visitor_number"],
        "Footer_2" : None,
        "datestamp" : visitor_data["datestamp"], 
        "dwell_time" : (visitor["end_time"] - visitor["start_time"]).seconds if visitor["end_time"] else 0, #guard 
    }



def _assemble_visitor_data(visitor):
    #pulls what is needed from visitor\
    
    return {
        "visitor_number": visitor["number"],
        #color - value - saturation
        "hue_category": visitor["hue_category"],
        "brightness": visitor["brightness"],
        #pose - face - body detected
        "face_detected" : visitor["face_detected"],
        "body_detected" :visitor["body_detected"],
        "hand_detected" : visitor["hand_detected"],
        #visitor identity 
        "visitor_number" : visitor["number"],
        "datestamp" : visitor["datestamp"],
        "start_time": visitor["start_time"],
        "end_time": visitor["end_time"],
        "dwell_time" : (visitor["end_time"] - visitor["start_time"].seconds if visitor["end_time"] else 0), #guard 
    }




def _assemble_decider_data(decider_output):
    
    
    visitor_lucky_number = decider_output["satisfaction_score"] 

    

    return {
        "lucky_number " : visitor_lucky_number
    }
