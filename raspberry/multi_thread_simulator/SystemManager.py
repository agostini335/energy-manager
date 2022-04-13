import time
import logging
class SystemManager():

    TEMP_GOAL = 51 #CELSIUS
    
    INIT_MAX_WAITING_TIME = 10 # secondi di attesa in INIT prima di passare ad Active o Timeout
    INIT_MIN_FRESH_READINGS = 3 # numero minimo di letture Fresh in INIT da ricevere per poter passare in Active

    TIMEOUT_TIME_BTWN_FRESH = 10 # secondi entro il quale vanno ricevute 2 letture Fresh per passare in Active o Temp Reached


    def __init__(self):
        pass
    def scarica(self):
        logging.info("SYTSTEM:scarica")
        time.sleep(6)
    def scarica_shutdown(self):
        logging.info("SYTSTEM:scaricashutdown")
        time.sleep(6)
    def up(self):
        logging.info("SYTSTEM:up")
        time.sleep(3)
    def down(self):
        logging.info("SYTSTEM:down")
        time.sleep(3)
    def releon(self):
        logging.info("SYTSTEM:releON")
        time.sleep(3)

    