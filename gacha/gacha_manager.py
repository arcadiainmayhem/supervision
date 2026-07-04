from gacha.gacha_constants import *
from datetime import datetime
import random

class GachaManager():



    def __init__(self):

        #flag if it has fired today
        self.has_fired_today = False
        self.last_fire_date = None

        self.daily_fire_count = 0    


    def check_gacha(self,visitor):

        self._check_date_reset()

        if self.daily_fire_count >= MAX_GACHA_WINNERS:
            return False
        
        #check current hour
        current_hour = datetime.now().hour
        #check window
        window = self._check_time_window()
        #check hit probabilty
        probabilty = self._get_hit_probability(window , current_hour)

        print(f"[GACHAMANAGER] Window : {window} | Hours : {current_hour }")
              
        roll = random.random()
        print(f"[GACHAMANAGER] Roll : {roll:.2f}")

        if roll < probabilty:
            self.daily_fire_count += 1
            print(f"[GACHAMANAGER] Gacha Triggered")
            return True        
            
        #most of the time false
        return False


    def _check_date_reset(self):
        today = datetime.now().date()

        if self.last_fire_date != today:
            self.has_fired_today = False
            self.daily_fire_count = 0
            self.last_fire_date = today 
            print('[GACHAMANAGER] New Date - Reset')


    def _check_time_window(self):
        current_hour = datetime.now().hour

        if current_hour < GACHA_WINDOW_START or current_hour >= GACHA_WINDOW_END:
            return None #outside of 10am - 7pm
        
        return "base"

    def _get_hit_probability(self , window , current_hour):
        #shouldnt just be random roll
        
        if window is None:
            return 0.0 #outside window
        
        #unsure about this 
        if current_hour >= GACHA_GUARANTEED_HOUR:
            return 0.95

        #base window - ramp increases each hour
        hours_elapsed = current_hour - GACHA_WINDOW_START
        probabilty = GACHA_BASE_PROBABLITY + (hours_elapsed * GACHA_RAMP_RATE)

        return min(probabilty , 0.95)