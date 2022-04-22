import serial
import time
import lcd_driver
import statistics
import RPi.GPIO as GPIO
import logging

class SystemManager():
    #general
    TEMP_GOAL = 55 #CELSIUS
    
    #init
    INIT_MAX_WAITING_TIME = 10 # secondi di attesa in INIT prima di passare ad Active o Timeout
    INIT_MIN_FRESH_READINGS = 2 # numero minimo di letture Fresh in INIT da ricevere per poter passare in Active

    #timeout
    TIMEOUT_TIME_BTWN_FRESH = 10 # secondi entro il quale vanno ricevute 2 letture Fresh per passare in Active o Temp Reached
    
    #tempreached
    TEMPREACHED_HISTERESYS = 5 # gradi di isteresi per uscire da tempreached es: temp_goal = 50, isteresi= 5 -> torno Active a 45 gradi
    TEMPREACHED_WAITING_TIME_TO = 10 # secondi dall'ultima lettura oltre il quale si passa in timeout

    #active
    ACTIVE_WAITING_TIME_TO = 10 # secondi dall'ultima lettura oltre il quale si passa in Timeout
    ACTIVE_MIN_IMMISSIONE = 100 # watt minimi di immissione per operare e non spegnere
    ACTIVE_MIN_IMMISSIONE_TO = 10 # secondi di attesa in no-immissione prima di spegnere il triac
    ACTIVE_NOISE_BOILER = 50 # watt di tolleranza oltre quali si considera il boiler spento e non si da il comando down
    ACTIVE_LIMITE_TRIAC = 2300 # watt max che puo raggiungere il triac
    ACTIVE_DELTA_MAX_TRIAC_UP = 100 #watt di distanza dal limite triac entro il quale non eseguiamo up per sicurezza
    ACTIVE_LOWERBOUND_IMM = 150 # watt minimi di immissione per essere in fascia goal
    ACTIVE_UPPERBOUND_IMM = 250 # watt massimi di immissione per essere in fascia goal

    #config
    RELE_STATE = True #TODO VERIFY

    #button
    BUTTON_TIME_SLEEP = 0.5
    BUTTON_PRESSED_WAIT = 3

    def __init__(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        

        self.ser = serial.Serial('/dev/ttyUSB0',9600)
        self.ser.ReadBufferSize = 20

        #GPIO CONFIG
        self.pin_rele = 16
        self.pin_up = 21
        self.pin_down =20
        self.pin_button = 15
        GPIO.setup(self.pin_rele,GPIO.OUT) #rele
        GPIO.setup(self.pin_up,GPIO.OUT) #up
        GPIO.setup(self.pin_down,GPIO.OUT) #down
        GPIO.setup(self.pin_button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #mod button
        GPIO.output(self.pin_rele,False)
        GPIO.output(self.pin_up,False)
        GPIO.output(self.pin_down,False)
    
    def scarica_shutdown(self):
        if self.RELE_STATE:
            logging.info("SYTSTEM: SCARICASHUTDOWN")
            GPIO.output(self.pin_up,True)
            time.sleep(1)
            GPIO.output(self.pin_down,False)	
            time.sleep(8)
            GPIO.output(self.pin_down,True)
            GPIO.output(self.pin_rele,False)
            self.RELE_STATE = False

    def releon(self):
        if not self.RELE_STATE:
            logging.info("SYTSTEM: RELEON")
            GPIO.output(self.pin_rele,True)            
            self.RELE_STATE = True

    def s_down(self):
        assert(self.RELE_STATE)
        logging.info("SYTSTEM:---DOWN---")
        GPIO.output(self.pin_down,False)
        time.sleep(0.2)
        GPIO.output(self.pin_down,True)

    def s_up(self):
        assert(self.RELE_STATE)
        logging.info("SYTSTEM:+++UP+++")
        GPIO.output(self.pin_up,False)
        time.sleep(0.2)
        GPIO.output(self.pin_up,True)

    def full_power(self):
        #TODO TO TEST
        assert(self.RELE_STATE)
        logging.info("SYTSTEM: FULL POWER")    
        # -> scarica    
        GPIO.output(self.pin_up,True)
        time.sleep(1)
        GPIO.output(self.pin_down,False)	
        time.sleep(8)
        GPIO.output(self.pin_down,True)
        # -> full_power
        GPIO.output(self.pin_up,False)
        time.sleep(15)
        GPIO.output(self.pin_up,True)
    
    def buttonIsHigh(self):
        return GPIO.input(self.pin_button) != GPIO.LOW

        

