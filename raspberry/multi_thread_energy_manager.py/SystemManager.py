import serial
import time
import lcd_driver
import statistics
import RPi.GPIO as GPIO

class SystemManager():
    def __init__(self) -> None:
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        self.ser = serial.Serial('/dev/ttyUSB0',9600)
        self.ser.ReadBufferSize = 30

        #GPIO CONFIG
        pin_rele = 16
        pin_up = 21
        pin_down =20
        GPIO.setup(pin_rele,GPIO.OUT) #rele
        GPIO.setup(pin_up,GPIO.OUT) #up
        GPIO.setup(pin_down,GPIO.OUT) #down
        GPIO.output(pin_rele,False)
        GPIO.output(pin_up,False)
        GPIO.output(pin_down,False)

        r_tensione = -1 	#tensione letta
        r_carico = -1   	#carico letto
        r_produzione = -1 	#produzione letta
        r_immissione = -1 	#immissione sonda letta
        r_boiler = -1 		#carico boiler letto
        r_temperatura =-1	#temperatura sonda letta
        stato_rele=True
        notimeout=True
        f_immissione=True
        temp_ok=False

        sum_temp = 0
        temp_counter = 0

        DOWN_GOAL=150
        UP_GOAL=220
        AVG_TEMP_WINDOW_LENGTH = 30 # Valori considerati nella media della temperatura
        ISTERESI_TEMPERATURA=4 #GRADI GOAL DI TEMPERATURA
        TEMPERATURA_GOAL=52 #GRADI GOAL DI TEMPERATURA
        MARGINE_IMMISSIONE = 100 	# WATT di margine
        LIMITE_TRIAC = 2300 #WATT max triac
        TIMEOUT = 20			#Secondi di Timeout consentiti perdita connessione radio
        TIMEOUT_IMMISSIONE = 20    #Secondi di Timeout consentiti assenza di immissione
        TIMEOUT_TEMP_OK = 5 #Secondi di timeout prima di staccare il rele a temperatura raggiunta
        last_time_read = time.time()
        current_milli_time =time.time()
        last_temp_ok =time.time()
        first_temp_ok =time.time()