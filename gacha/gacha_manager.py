from gacha.gacha_constants import *
from datetime import datetime
import random

class GachaManager():



    def __init__(self):

        #flag if it has fired today
        self.has_fired_today = False
        self.last_fire_date = None





    def check_gacha(self, visitor):


        #if already fired, automatic false
        if self.has_fired_today:
            return False
        #check current day
        self._check_date_reset()

        #check current hour
        current_hour = datetime.now().hour
        #check window
        window = self._check_time_window()
        #check probabilty
        probability = self._get_hit_probability(window , current_hour)

        print(f"[GACHAMANAGER] Window : {window} | Hours : {current_hour }")
              
        roll = random.random()
        print(f"[GACHAMANAGER] Roll : {roll:.2f}")

        if roll < probability:
            self.has_fired_today = True
            self.last_fire_date = datetime.now().date()
            print(f"[GACHAMANAGER] Gacha Triggered")
            return True

    
        #for testing
        #return True
        return False

    def _check_date_reset(self):
        today = datetime.now().date()

        if self.last_fire_date != today:
            self.has_fired_today = False
            self.last_fire_date =today

            print('[GACHAMANAGER] New Date - Reset')


    def _check_time_window(self):
        current_hour = datetime.now().hour

        if current_hour < GACHA_PEAK_START or current_hour >= GACHA_PEAK_END:
            return None #outside of peak hour

        if GACHA_PEAK_START <= current_hour < GACHA_PEAK_END: #current house > 1pm and < 5pm
            return "peak"
        
        return "base"

    def _get_hit_probability(self , window , current_hour):
        #shouldnt just be random roll
        
        if window is None:
            return 0.0 #outside window
        
        #unsure about this 
        if current_hour >= GACHA_GUARANTEED_HOUR:
            return 1.0
        
        if window == "peak":
            return GACHA_PEAK_PROBABILITY
        

        #base window - ramp increases each hour
        hours_elapsed = current_hour - GACHA_WINDOW_START
        probabilty = GACHA_BASE_PROBABLITY + (hours_elapsed * GACHA_RAMP_RATE)

        return min(probabilty , 1.0)