from .obelisk_director import ObeliskDirector
from .minilisk_director import MiniliskDirector
from core.visitor_state import create_visitor_state
from core.decider.installation_decider import decide_score
from hardware.button.button_listener import start
from datetime import datetime

#main coordinator 

class InstallationDirector :
    
    def __init__(self):
        #stores references to other directors
        #start + store instance of Director - Only one
        self.obelisk_director = ObeliskDirector()
        self.minilisk_director =  MiniliskDirector()
        
        #hardware
        #button related
        self.isButtonActive = False
        self.isButtonListening = False

        #printer related
        
        #visitor related
        self.current_visitor = None
        self.current_visitor_score = None
        self.encounter_history = []

        #starts installation -> starts directors | creates visitor when new one comes in frame | receives output / data from directors -> decides on type of output
        self.isActive = False
        self.isDeciding = False
        self.is_encounter_running = False
        #to store # of decisions made during installation
        self.madeDecision = False
        self.decision_count = 0
       

    #installtion goes live
    def start(self):
        self.isActive = True
        #button listener
        self.obelisk_director.start_watching()
        #setup button listener + initialise
        start(self._run_encounter)
        #signal to printer that its ready

        #signal to microphone 

    def create_visitor(self):
        id_number = self.determine_visitor_id() #dont need null check as 0 + 1 at the start
        visitor = create_visitor_state(id_number)
        return visitor
    
    

    #pause
    def stop(self):
        self.isActive = False
        #tell obelisk to stop watching
        #button on standby
        #release camera
        self.obelisk_director._stop_camera()
        #stop printers

    #full shutdown
    def shutdown(self):
        self.stop()
        #additional cleanup

    def determine_visitor_id(self):
        return len(self.encounter_history ) + 1

    def _run_encounter(self, channel = None):
        #channel might be a GPIO pin number , a keyboard event or None
        #we dont use it, but accept it gracefully

        #check button press / trigger -> gets observation visitor dict from obelisk
        #create visitor
        #guard against running twice
        if self.is_encounter_running:
            return
        self.is_encounter_running = True
        self.current_visitor =  self.create_visitor()

        self.obelisk_director.observe(self.current_visitor) #captures frame and runs pipeline
        
        self._evaluate_visitor_profile(self.current_visitor)
        
        self._route_output(self.current_visitor)
        print('Route Output Done')
        #add visitor to history to measure length
        self._add_to_visitor_history(self.current_visitor)
        print('History Added')
        #log endtime
        self.current_visitor["end_time"] = datetime.now()
        #reset and prepare for next visitor
        self._reset()
        print('Reset Done')
       

    def _evaluate_visitor_profile(self, visitor):
        #brain + determines if its selphy , or thermal
        self.current_visitor_score = decide_score(visitor)
        print("Score: ", self.current_visitor_score)
    
    def _add_to_visitor_history(self,visitor):
        self.encounter_history.append(visitor)

    def _route_output(self , visitor):
        #decide which to print
        # if self.current_visitor_score["printer_output_type"] == "selphy":
        #     print("Printing Selphy Card")
        self.obelisk_director.produce_selphy_card(visitor)
        # elif self.current_visitor_score["printer_output_type"] == "thermal":

        #self.minilisk_director.produce_thermal_slip(visitor, self.current_visitor_score)

    def _reset(self):
        self.current_visitor = None
        self.current_visitor_score = None
        self.is_encounter_running = False
     