from directors.installation_director import InstallationDirector
#from hardware.button.button_listener import register_shutdown_button
import time
from core.installation_constants import *



def main():



    installation = InstallationDirector()
    installation.start()
    print("Installation is Active")

    #register_shutdown_button(installation.shutdown)

    #stress test
    if STRESS_TEST:
        installation.start_stress_test()
    
    #keep alive
    try:
        while True:

            time.sleep(0.1)

        

    except KeyboardInterrupt:
        installation.exit_program()
        print("Installation Shutdown Cleanly")    




if __name__ == "__main__":
    main()