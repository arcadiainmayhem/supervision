from led_states import LEDState
from hardware_config import *
from core.installation_constants import *
import threading
import time
from led_constants import *

#only on pi
if not DEV_MODE:
    from rpi_ws281x import PixelStrip , Color

class LEDManager():


    def __init__(self):
        self.current_state = LEDState.IDLE
        self.stop_animation = False #flag for stopping animation
        self.animation_thread = None
        
        #only on pi
        if not DEV_MODE:
            self.strip = PixelStrip(LED_COUNT , LED_SIGNAL_PIN, brightness = BRIGHTNESS )
            self.strip.begin()

    def set_state(self , state : LEDState):
        self.stop_animation = True #stops current LED state animation 

        #if something is going on
        if self.animation_thread:
            self.animation_thread.join() #waits for current thread to finish

        self.stop_animation = False # reset flag
        self.current_state = state #blank

        self.animation_thread = threading.Thread(target = self._animate,
                                              args=(state,))
        self.animation_thread.daemon = True #means that its a background thread
        self.animation_thread.start()

    def _animate(self , state : LEDState):    
        if DEV_MODE:
            print(f"[LEDMANAGER] : current state {state}")
            return
        
        match state:
            case LEDState.IDLE:
                color = STATE_COLORS["idle"]
                while not self.stop_animation:
                    self._fade_in(color)
                    self._fade_out(color)
                    time.sleep(SLEEP_TIME)

            case LEDState.TRIGGERED:
                color = STATE_COLORS["triggered"]
                self._flash(color, FLASH_TIMES)
                time.sleep(SLEEP_TIME)
                
            case LEDState.PROCESSING:
                # shift
                color = STATE_COLORS["processing"]
                while not self.stop_animation:
                    self._chase(color)
                
            case LEDState.PRINTING:
                # steady colour
                color = STATE_COLORS["printing"]
                while not self.stop_animation:

                    self._steady(color)
                    time.sleep(SLEEP_TIME)

            case LEDState.COMPLETED:
                # brief flash then idle
                color = STATE_COLORS["completed"]
                self._pulse(color)

            case LEDState.ERROR:
                color = STATE_COLORS["error"]
                # steady red
                while not self.stop_animation:
                    self._steady(color)
                    time.sleep(SLEEP_TIME)

            case LEDState.BORED:
                # animated loop
                color = STATE_COLORS["bored"]
                while not self.stop_animation:
                    self._pulse(color)
                    time.sleep(SLEEP_TIME)
                    
            case LEDState.SATAN:
                # fire cycle
                print("Animating SATAN LED State")
                pass




    def _set_all(self , r,g,b):
        for i in range (LED_COUNT):
            self.strip.setPixelColor(i,Color(r,g,b))
        self.strip.show()



    def _fade_in(self, color):
        r  , g , b = color
        for brightness in range (0,255,5):

            #return early 
            if self.stop_animation:
                return

            factor = brightness/255
            self._set_all(int(r*factor) , int(g*factor), int(b*factor))
            time.sleep(0.02)


    
    def _fade_out(self, color):
        r  , g , b = color
        for brightness in range (255,0,-5):

            #return early 
            if self.stop_animation:
                return
            
            factor = brightness/255
            self._set_all(int(r*factor) , int(g*factor), int(b*factor))
            time.sleep(0.02)


    def _flash(self, color , times):       
        for _ in range (times):

            #return early 
            if self.stop_animation:
                return
            
            
            self._set_all(*color)
            time.sleep(0.1)
            self._set_all(0 , 0 , 0 )
            time.sleep(0.1)





    def _steady(self , color):
        r , g, b = color
        
        self._set_all(int(r) , int(g), int(b))

    def _pulse(self, color):
        self._fade_in(color)
        self._fade_out(color)

    def _chase(self, color):
        for i in range(LED_COUNT):
            if self.stop_animation:
                return
            
            self._set_all(0,0,0) #clear all

            self.strip.setPixelColor(i , Color(*color)) #lights # led according to i
            self.strip.show()
            time.sleep(0.1)
        