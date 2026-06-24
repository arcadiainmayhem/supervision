from hardware.led.led_states import LEDState
from hardware.hardware_config import *
from core.installation_constants import *
import threading
import time
from hardware.led.led_constants import *

#only on pi
if not DEV_MODE:
    import serial #to communicate with ESP Receiver


class LEDManager():


    def __init__(self):
        self.current_state = LEDState.IDLE
        self.port = SERIAL_PORT
        self.baud = BAUD_RATE

        # only on pi
        if not DEV_MODE:
            print("[LEDMANAGER] DEBUG - Attempting serial init")
            try:
                self.serial = serial.Serial(self.port, self.baud, timeout=1)
                print("[LEDMANAGER] Serial to ESP32 B Ready")
            except Exception as e:
                self.serial = None
                print(f"[LEDMANAGER] Serial init Failed : {e}")
        else:
            self.serial = None

    def set_state(self, state: LEDState):
        self.current_state = state
        self._send_to_esp32(state)

    def _send_to_esp32(self, state: LEDState):
        if DEV_MODE:
            print(f"[LEDMANAGER] ESP32 State: {state.value.upper()}")
            return

        if self.serial:
            try:
                self.serial.write(f"{state.value.upper()}\n".encode())
            except (OSError, serial.SerialException) as e:
                print(f"[LEDMANAGER] Serial write failed: {e} - reconnecting")
                self._reconnect()
                try:
                    self.serial.write(f"{state.value.upper()}\n".encode())
                except (OSError, serial.SerialException) as e2:
                    print(f"[LEDMANAGER] Retry failed: {e2}")

    def _reconnect(self):
        try:
            if self.serial and self.serial.is_open:
                self.serial.close()
        except Exception:
            pass

        try:
            self.serial = serial.Serial(self.port, self.baud, timeout=1)
            print("[LEDMANAGER] Serial Reconnected")
        except Exception as e:
            print(f"[LEDMANAGER] Reconnect failed : {e}")
            self.serial = None



    # def __init__(self):
    #     self.current_state = LEDState.IDLE
    #     self.stop_animation = False #flag for stopping animation
    #     self.animation_thread = None
    #     self.port = SERIAL_PORT
    #     self.baud = BAUD_RATE

    #     #only on pi
    #     if not DEV_MODE:
    #         self.strip = PixelStrip(LED_COUNT , LED_SIGNAL_PIN, brightness = BRIGHTNESS , channel = LED_CHANNEL )
    #         self.strip.begin()
    #         print("[LEDMANAGER] DEBUG - Attempting serial init")
    #         try:
    #             self.serial = serial.Serial( SERIAL_PORT , 
    #                                         115200 , 
    #                                         timeout= 1)
    #             print("[LEDMANAGER] Serial to ESP32 B Ready")
    #         except Exception as e:
    #             self.serial = None
    #             print(f"[LEDMANAGER] Serial init Failed : {e}")

    # def set_state(self , state : LEDState):
    #     self.stop_animation = True #stops current LED state animation 

    #     #if something is going on
    #     if self.animation_thread:
    #         self.animation_thread.join() #waits for current thread to finish

    #     self.stop_animation = False # reset flag
    #     self.current_state = state #blank

    #     self.animation_thread = threading.Thread(target = self._animate,
    #                                           args=(state,))
    #     self.animation_thread.daemon = True #means that its a background thread
    #     self.animation_thread.start()


    #     #send to esp32
    #     self._send_to_esp32(state)
        

    # def _send_to_esp32(self,state:LEDState):
    #     if DEV_MODE:
    #        print(f"[LEDMANAGER] ESP32 State: {state.value.upper()}")
    #        return 

    #     if self.serial:
    #         try:
    #             self.serial.write(f"{state.value.upper()}\n".encode())
    #             #catching OS error
    #         except (OSError , serial.SerialException) as e:
    #             print(f"[LEDMANAGER] Serial write failed: {e} - reconnecting")
    #             #tries to reconnect 
    #             self._reconnect()
    #             try:
    #                 self.serial.write(f"{state.value.upper()}\n".encode())
    #             except (OSError, serial.SerialException) as e2:
    #                     print(f"[LEDMANAGER] Retry failed: {e2}")

    # def _reconnect(self):
    #     try:
    #         if self.serial and self.serial.is_open:
    #             self.serial.close()
    #     except Exception:
    #         pass

    #     try:
    #         self.serial = serial.Serial(self.port,self.baud,timeout=1)
    #         print("[LEDMANAGER] Serial Reconnected")
    #     except Exception as e:
    #         print(f"[LEDMANAGER] Reconnect failed : {e}")
    #         self.serial = None




    # def _animate(self , state : LEDState):    
    #     if DEV_MODE:
    #         print(f"[LEDMANAGER] : current state {state}")
    #         return
        
    #     match state:
    #         case LEDState.IDLE:
    #             color = STATE_COLORS["idle"]
    #             while not self.stop_animation:
    #                 self._fade_in(color)
    #                 self._fade_out(color)
    #                 time.sleep(SLEEP_TIME)

    #         case LEDState.TRIGGERED:
    #             color = STATE_COLORS["triggered"]
    #             self._flash(color, FLASH_TIMES)
    #             time.sleep(SLEEP_TIME)
                
    #         case LEDState.PROCESSING:
    #             # shift
    #             color = STATE_COLORS["processing"]
    #             while not self.stop_animation:
    #                 self._chase(color)
                
    #         case LEDState.PRINTING:
    #             # steady colour
    #             color = STATE_COLORS["printing"]
    #             while not self.stop_animation:

    #                 self._steady(color)
    #                 time.sleep(SLEEP_TIME)

    #         case LEDState.COMPLETED:
    #             # brief flash then idle
    #             color = STATE_COLORS["completed"]
    #             self._pulse(color)

    #         case LEDState.ERROR:
    #             color = STATE_COLORS["error"]
    #             # steady red
    #             while not self.stop_animation:
    #                 self._steady(color)
    #                 time.sleep(SLEEP_TIME)

    #         case LEDState.BORED:
    #             # animated loop
    #             color = STATE_COLORS["bored"]
    #             while not self.stop_animation:
    #                 self._pulse(color)
    #                 time.sleep(SLEEP_TIME)

    #         case LEDState.GACHA:
    #             color = STATE_COLORS["gacha"]
    #             for _ in range(3):
    #                 if self.stop_animation:
    #                     return
    #                 self._pulse(color)
                    
    #         case LEDState.SATAN:
    #             # fire cycle
    #             print("Animating SATAN LED State")
    #             pass



    # def _set_all(self , r,g,b):
    #     for i in range (LED_COUNT):
    #         self.strip.setPixelColor(i,Color(r,g,b))
    #     self.strip.show()



    # def _fade_in(self, color):
    #     r  , g , b = color
    #     for brightness in range (0,255,5):

    #         #return early 
    #         if self.stop_animation:
    #             return

    #         factor = brightness/255
    #         self._set_all(int(r*factor) , int(g*factor), int(b*factor))
    #         time.sleep(0.02)


    
    # def _fade_out(self, color):
    #     r  , g , b = color
    #     for brightness in range (255,0,-5):

    #         #return early 
    #         if self.stop_animation:
    #             return
            
    #         factor = brightness/255
    #         self._set_all(int(r*factor) , int(g*factor), int(b*factor))
    #         time.sleep(0.02)


    # def _flash(self, color , times):       
    #     for _ in range (times):

    #         #return early 
    #         if self.stop_animation:
    #             return
            
            
    #         self._set_all(*color)
    #         time.sleep(0.1)
    #         self._set_all(0 , 0 , 0 )
    #         time.sleep(0.1)



    # def _steady(self , color):
    #     r , g, b = color
        
    #     self._set_all(int(r) , int(g), int(b))

    # def _pulse(self, color):
    #     self._fade_in(color)
    #     self._fade_out(color)

    # def _chase(self, color):
    #     for i in range(LED_COUNT):
    #         if self.stop_animation:
    #             return
            
    #         self._set_all(0,0,0) #clear all

    #         self.strip.setPixelColor(i , Color(*color)) #lights # led according to i
    #         self.strip.show()
    #         time.sleep(0.1)