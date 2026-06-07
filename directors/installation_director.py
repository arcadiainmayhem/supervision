import os 
import signal
import traceback
import time
import threading

from directors.obelisk_director import ObeliskDirector

from core.visitor_state import create_visitor_state
from core.decider.installation_decider import decide
from core.installation_constants import *

from computervision.interpreter.interpretation_director import intepret_everything
from hardware.button.button_listener import register_trigger_button
from datetime import datetime
from core.save_manager import save

from hardware.led.led_manager import LEDManager
from hardware.led.led_states import LEDState

from gacha.gacha_manager import GachaManager
from gacha.gacha_compositor import get_golden

from monitoring.status_server import start_in_thread
from monitoring import status_logger
#main coordinator 

class InstallationDirector :
    
    def __init__(self):
        #stores references to other directors
        #start + store instance of Director - Only one
        self.obelisk_director = ObeliskDirector()
        #start one instance of LEDManager
        self.led_manager = LEDManager()
        #instance of Gacha Manager
        self.gacha_manager = GachaManager()
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


        #set initial led state to idle
        self.led_manager.set_state(LEDState.IDLE)

        #start thread for server monitoring
        start_in_thread()
        print(f"[INSTALLTIONDIECTOR] Status serve stated on port, {STATUS_SERVER_PORT}")

    #installation goes live
    def start(self):
        self.isActive = True
        #button listener
        #setup button listener + initialise
        register_trigger_button(self._run_encounter)

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
            #[UPDATE SERVER STATUS]
            status_logger.update_status("state" , "triggered")

            #[ENCOUNTER TRIGGERED]
            self.led_manager.set_state(LEDState.TRIGGERED)
            #[VISITOR CREATED]
            self.current_visitor =  self.create_visitor()

            self.obelisk_director.observe(self.current_visitor) #captures frame and runs pipeline
            #[UPDATE SERVER STATUS]
            status_logger.update_status("state" , "processing")        
            #intepret and store in visitor dict
            intepret_everything(self.current_visitor)

            #[PROCESSING ENCOUNTER TRIGGERED]
            self.led_manager.set_state(LEDState.PROCESSING)
            self._evaluate_visitor_profile(self.current_visitor) #decide + score value type

            #select elements for selphy
            self.obelisk_director.select_elements(self.current_visitor)
   
            #select printer
            success = self._route_output(self.current_visitor)

            #[EARLY RETURN IF NOT SUCCESS]
            if not success:
                print(f"[INSTALLATIONDIRECTOR] Print failed — resetting debounce for retry ")
                self.last_trigger_time = PRINT_ERROR_COOLDOWN #allows immediate retry
                status_logger.update_status("state" , "error")

            #[UPDATE SERVER STATUS]
            status_logger.log_encounter(self.current_visitor)
            status_logger.update_status("state" , "printing")     
            #[COMPLETED TRIGGERED]
            self.led_manager.set_state(LEDState.COMPLETED)
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
            self.led_manager.set_state(LEDState.ERROR)

            print(f"Encounter Failed: {e}")
            #[UPDATE SERVER STATUS]
            status_logger.log_error(f"Installation Director: " ,str(e)) 
            status_logger.update_status("state" , "error")
 
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
        print("Satisfaction Score:", visitor["satisfaction_score"])
        print("Unlocked Rarities:", visitor["unlocked_rarity_tier"])
        print("Output:", visitor["output_type"])

    
    def _add_to_visitor_history(self,visitor):
        self.encounter_history.append(visitor)

    def _route_output(self , visitor):

        self.led_manager.set_state(LEDState.PRINTING)

        if visitor["output_type"] == "selphy":
            image = self.obelisk_director.composite_selphy_card(visitor)
            #save to visitor dict 
            visitor["output_path"] = save(image, visitor , "selphy")
         
            #check gacha 

            if self.gacha_manager.check_gacha(visitor):
                try:
                    #gets Golden Gacha Output Path
                    golden_path = get_golden()
                    if golden_path: #incase theres an error
                        self.led_manager.set_state(LEDState.GACHA)

                        print("[INSTALLATIONDIRECTOR] Corrupting Image ~ Getting Golden")
                        #overrides
                        visitor["output_path"] = golden_path
                except Exception as e:
                    print(f"[INSTALLATIONDIRECTOR] Gacha Corruption Failed : {e} - printing normal card")

            #print after saving from path

            success = self.obelisk_director.prepare_selphy_card_print(visitor)

            return success



    def _reset(self):
        self.led_manager.set_state(LEDState.IDLE)
        self.current_visitor = None
        self.current_visitor_score = None
        self.is_encounter_running = False
     

         #pause
    def stop(self):
        self.isActive = False
        #tell obelisk to stop watching
        #stop printers

    #full shutdown
    def shutdown(self , channel = None):
        self.stop()
        #additional cleanup + cleanup for
        #shutdown os
        os.system("sudo shutdown now")

    def _auto_trigger_loop(self):
        for i in range(STRESS_TEST_MAX_TRIGGERS):
            print(f"[INSTALLATIONDIRECTOR][STRESSTEST] Auto trigger {i+1} of {STRESS_TEST_MAX_TRIGGERS}")
            self._run_encounter()
            time.sleep(STRESS_TEST_INTERVALS)

    def start_stress_test(self):
        thread = threading.Thread(
            target = self._auto_trigger_loop,
            args=(STRESS_TEST_INTERVALS , STRESS_TEST_MAX_TRIGGERS)
        )
        thread.daemon = True
        thread.start()

    #debuggin
    def exit_program(self):
        self.stop()
        os.kill(os.getpid(), signal.SIGINT)