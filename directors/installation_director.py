from .obelisk_director import ObeliskDirector
from .minilisk_director import MiniliskDirector
from core.visitor_state import create_visitor_state
from core.decider.installation_decider import decide
from core.installation_constants import *
from computervision.interpreter.interpretation_director import intepret_everything
from hardware.button.button_listener import register_trigger_button
from datetime import datetime
from core.save_manager import save
import os 
import signal
import traceback
import time

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
        self.is_printing = False
        self.last_trigger_time = 0
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
        register_trigger_button(self._run_encounter)

        #signal to printer that its ready

        #signal to microphone 

    def create_visitor(self):
        id_number = self.determine_visitor_id() #dont need null check as 0 + 1 at the start
        visitor = create_visitor_state(id_number)
        return visitor
    
    
    def determine_visitor_id(self):
        return len(self.encounter_history ) + 1

    def _run_encounter(self, channel = None):
        #channel might be a GPIO pin number , a keyboard event or None
        #we dont use it, but accept it gracefully
        print("Button Pressed - Encounter Triggered")
        print(f"_run_encounter called at {time.time()}")
        
        now = time.time()

        if now - self.last_trigger_time < TRIGGER_DEBOUNCE_SECONDS:
            print("Too Soon - Trigger Ignored")
            return



        #check button press / trigger -> gets observation visitor dict from obelisk
        #create visitor + guard against running twice
        if self.is_encounter_running or self.is_printing:
            print("Busy - Trigger Ignored")
            return
        
        self.last_trigger_time = now

        #setting flags to true
        self.is_encounter_running = True
        self.is_printing = True
        try:
            self.current_visitor =  self.create_visitor()

            self.obelisk_director.observe(self.current_visitor) #captures frame and runs pipeline
        
            #intepret and store in visitor dict
            intepret_everything(self.current_visitor)

            self._evaluate_visitor_profile(self.current_visitor) #decide + score value type
            #select elements for selphy
            self.obelisk_director.select_elements(self.current_visitor)
            #select readings for thermal
            self.minilisk_director.assemble_slip(self.current_visitor)
        

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

        except Exception as e:
            print(f"Encounter Failed: {e}")
            #prints full error with exact file
            traceback.print_exc()
        finally:
            #resets flags so it can be triggered again
            self.last_trigger_time = time.time()
            print("Last Trigger Time: ", self.last_trigger_time)


            self.is_encounter_running = False
            self.is_printing = False
            #clears buffer + registers
            print("Button Buffer Cleared")
            #register_trigger_button(self._run_encounter)

    def _evaluate_visitor_profile(self, visitor):
        #brain + determines if its selphy , or thermal
        decide(visitor)
        print("Score:", visitor["satisfaction_score"])
        print("Rarity:", visitor["rarity_tier"])
        print("Output:", visitor["output_type"])
    
    def _add_to_visitor_history(self,visitor):
        self.encounter_history.append(visitor)

    def _route_output(self , visitor):

        if visitor["output_type"] == "selphy":
            image = self.obelisk_director.composite_selphy_card(visitor)
            #save to visitor dict 
            visitor["output_path"] = save(image, visitor , "selphy")
            #print after saving from path
            self.obelisk_director.prepare_selphy_card_print(visitor)

        elif visitor["output_type"] == "thermal":
            # image = self.minilisk_director.composite_thermal_slip(visitor)
            # #save to visitor dict 
            # visitor["output_path"] = save(image, visitor , "thermal")
            # #print after saving from path
            # self.minilisk_director.prepare_thermal_slip_print(visitor)

            image = self.obelisk_director.composite_selphy_card(visitor)
            #save to visitor dict 
            visitor["output_path"] = save(image, visitor , "selphy")
            #print after saving from path
            self.obelisk_director.prepare_selphy_card_print(visitor)

    def _reset(self):
        self.current_visitor = None
        self.current_visitor_score = None
        self.is_encounter_running = False
     

         #pause
    def stop(self):
        self.isActive = False
        #tell obelisk to stop watching
        #button on standby
        #release camera
        self.obelisk_director._stop_camera()
        #stop printers

    #full shutdown
    def shutdown(self , channel = None):
        self.stop()
        #additional cleanup
        #cleanup for
        #shutdown os
        os.system("sudo shutdown now")


    #debuggin
    def exit_program(self):
        self.stop()
        os.kill(os.getpid(), signal.SIGINT)