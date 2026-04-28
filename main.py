from directors.installation_director import InstallationDirector
import time




def main():
    installation = InstallationDirector()
    installation.start()
    print("Installation is Active")


    #keep alive
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        installation.shutdown()
        print("Installation Shutdown Cleanly")    




if __name__ == "__main__":
    main()