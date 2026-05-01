from directors.installation_director import InstallationDirector
from hardware.button.button_listener import register_shutdown_button
import time




def main():
    installation = InstallationDirector()
    installation.start()
    print("Installation is Active")

    register_shutdown_button(installation.shutdown)
    #keep alive
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        installation.shutdown()
        print("Installation Shutdown Cleanly")    




if __name__ == "__main__":
    main()