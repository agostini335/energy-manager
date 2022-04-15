import time
import logging
class SystemManager():

    #general
    TEMP_GOAL = 51 #CELSIUS
    
    #init
    INIT_MAX_WAITING_TIME = 10 # secondi di attesa in INIT prima di passare ad Active o Timeout
    INIT_MIN_FRESH_READINGS = 2 # numero minimo di letture Fresh in INIT da ricevere per poter passare in Active

    #timeout
    TIMEOUT_TIME_BTWN_FRESH = 10 # secondi entro il quale vanno ricevute 2 letture Fresh per passare in Active o Temp Reached
    
    #tempreached
    TEMPREACHED_HISTERESYS = 4 # gradi di isteresi per uscire da tempreached es: temp_goal = 50, isteresi= 5 -> torno Active a 45 gradi
    TEMPREACHED_WAITING_TIME_TO = 10 # secondi dall'ultima lettura oltre il quale si passa in timeout

    #active
    ACTIVE_WAITING_TIME_TO = 10 # secondi dall'ultima lettura oltre il quale si passa in Timeout
    ACTIVE_MIN_IMMISSIONE = 100 # watt minimi di immissione per operare e non spegnere
    ACTIVE_MIN_IMMISSIONE_TO = 10 # secondi di attesa in no-immissione prima di spegnere il triac
    ACTIVE_NOISE_BOILER = 25 # watt di tolleranza oltre quali si considera il boiler spento e non si da il comando down
    ACTIVE_LIMITE_TRIAC = 2300 # watt max che può raggiungere il triac
    ACTIVE_DELTA_MAX_TRIAC_UP = 100 #watt di distanza dal limite triac entro il quale non eseguiamo up per sicurezza
    ACTIVE_LOWERBOUND_IMM = 150 # watt minimi di immissione per essere in fascia goal
    ACTIVE_UPPERBOUND_IMM = 250 # watt massimi di immissione per essere in fascia goal

    #config
    RELE_STATE = True #TODO VERIFY

    def __init__(self):
        pass

    def scarica_shutdown(self):
        if self.RELE_STATE:
            logging.info("SYTSTEM: SCARICASHUTDOWN")
            time.sleep(6)
            self.RELE_STATE = False
    def releon(self):
        if not self.RELE_STATE:
            logging.info("SYTSTEM: RELEON")
            time.sleep(3)
            self.RELE_STATE = True
    def s_down(self):
        assert(self.RELE_STATE)
        logging.info("SYTSTEM:---DOWN---")
        time.sleep(3)
    def s_up(self):
        assert(self.RELE_STATE)
        logging.info("SYTSTEM:+++UP+++")
    def full_power(self):
        assert(self.RELE_STATE)
        logging.info("SYTSTEM: FULL POWER")

    