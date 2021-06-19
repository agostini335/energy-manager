import serial
import time
#import lcddriver
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
print("start")
ser = serial.Serial('/dev/ttyUSB0',9600)
ser.ReadBufferSize = 30
#display = lcddriver.lcd()

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

DOWN_GOAL=150
UP_GOAL=220
ISTERESI_TEMPERATURA=4 #GRADI GOAL DI TEMPERATURA
TEMPERATURA_GOAL=55 #GRADI GOAL DI TEMPERATURA
MARGINE_IMMISSIONE = 100 	# WATT di margine
LIMITE_TRIAC = 2300 #WATT max triac
TIMEOUT = 20			#Secondi di Timeout consentiti perdita connessione radio
TIMEOUT_IMMISSIONE = 20    #Secondi di Timeout consentiti assenza di immissione
TIMEOUT_TEMP_OK = 5 #Secondi di timeout prima di staccare il rele a temperatura raggiunta
last_time_read = time.time()
current_milli_time =time.time()
last_temp_ok =time.time()
first_temp_ok =time.time()
#display = lcddriver.lcd()
def gPrint(r_tensione,r_carico,r_produzione,r_immissione,r_boiler,r_temperatura):
    pass
    r1="rete: "+str(r_tensione)+" car: "+str(r_carico)
    r2="prd: "+str(r_produzione)+" imm: "+str(r_immissione)
    r3="boi: "+str(r_boiler)+" tmp: "+str(r_temperatura)    
    display.lcd_display_string(str(r1), 1) 
    display.lcd_display_string(str(r2), 2)
    display.lcd_display_string(str(r3), 3) 


print("start")


def up():
    GPIO.output(pin_up,True)
def down():
    GPIO.output(pin_down,True)
def stop():
    GPIO.output(pin_up,False)
    GPIO.output(pin_down,False)
def shut_down():
    print("SHUTDOWN")    
    GPIO.output(pin_rele,False)
    stop()
    
    
def releon():
	GPIO.output(pin_rele,True)
	stato_rele=True

def s_up():	
	if(stato_rele):
		GPIO.output(pin_up,True)
		time.sleep(0.2)
		GPIO.output(pin_up,False)
	

def s_down():
	if(stato_rele):	
		GPIO.output(pin_down,True)
		time.sleep(0.2)
		GPIO.output(pin_down,False)

def scarica():
	print("SCARICO")	
	GPIO.output(pin_up,False)
	time.sleep(1)
	GPIO.output(pin_down,True)
	time.sleep(6)
	GPIO.output(pin_down,False)	

def scarica_shutdown():
	print("SCARICO")	
	GPIO.output(pin_up,False)
	time.sleep(1)
	GPIO.output(pin_down,True)	
	time.sleep(6)
	GPIO.output(pin_down,False)
	GPIO.output(pin_rele,False)
        
time_no_immissione= 0
last_immissione_ok= 0    

  
def do_logic(carico,produzione,immissione,boiler,temperatura):
	immissione = immissione
	print("-------------------------------------------------------------->"+str(immissione))
	global time_no_immissione,last_immissione_ok,stato_rele, f_immissione, temp_ok, first_temp_ok,last_temp_ok
	if(immissione<100):		
		time_no_immissione = time.time()
		if(( time_no_immissione- last_immissione_ok)>TIMEOUT_IMMISSIONE):
			if(f_immissione):
				print("NO IMMISSIONE")					
				stato_rele=False
				scarica_shutdown()
				f_immissione=False			
				return
			print("STATO NO IMMISSIONE")			 
			return
	else:
		f_immissione=True
		last_immissione_ok =time.time()
		if(notimeout):
			stato_rele=True	
			releon()
	if ( temperatura>= TEMPERATURA_GOAL):
		print("TEMPERATURA RAGGIUNTA")		
		if(temp_ok == False):
			temp_ok=True
			first_temp_ok=time.time()	
					
		last_temp_ok=time.time()
		if(stato_rele):	
			if(last_temp_ok-first_temp_ok>TIMEOUT_TEMP_OK):
				print("TEMPERATURA RAGGIUNTA TIME-----------> SPEGNERE")				 
				stato_rele=False
				scarica_shutdown()					
		return				
	if ( boiler>=LIMITE_TRIAC or immissione<150):
		if(boiler>=25):
			s_down()
		print("DOWN")		
		return
				
	if boiler>LIMITE_TRIAC-100 and boiler <LIMITE_TRIAC :
		print("----------------------------------------------------------->GOAL")
		return	
	#fascia goal
	if immissione>=DOWN_GOAL and immissione <=UP_GOAL :
		print("----------------------------------------------------------->FASCIA GOAL")
		return	

	if boiler<LIMITE_TRIAC and temperatura<=TEMPERATURA_GOAL-ISTERESI_TEMPERATURA:
		s_up()
		print("UP")
		return 
	if temperatura<=TEMPERATURA_GOAL-ISTERESI_TEMPERATURA:
		temp_ok=False


last_immissione_ok=0   
releon()
scarica()
i=0
while 1:
	if(ser.in_waiting>0):
            i=i+1
            line = ser.readline()
            # CONVERSIONE STRINGA
            line=line[:-2] #removing last chars
            try:
				line_split = line.decode().split(';')
				# CHECK VALIDITA' STRINGA
				if ( len(line_split) == 7 and line_split[0]=='1' ):
					last_time_read=time.time()
					if(f_immissione and not temp_ok):
						releon()
						notimeout=True
						stato_rele=True
					#CONVERSIONE STRINGA COMPLETA
					r_tensione = int(line_split[1])
					r_carico =   int(line_split[2])
					r_produzione = int(line_split[3])
					r_immissione = int(line_split[4])
					r_boiler = int(line_split[5])
					r_temperatura = float(line_split[6])
					print(line_split)
					#gPrint(r_tensione,r_carico,r_produzione,r_immissione,r_boiler,r_temperatura)				
				if ( len(line_split) == 2 and line_split[0]=='0'):
					#CONVERSIONE BOILER				
					r_boiler = int(line_split[1])			
					print(line_split)					
				if(i==6):
					do_logic(r_carico,r_produzione,r_immissione,r_boiler,r_temperatura)
					i=0
            except:
				print("ciao")
	#CHECK TIMEOUT
	if(f_immissione and not temp_ok):
		current_milli_time=time.time()
		if(current_milli_time-last_time_read>TIMEOUT):
			print("TIMEOUT")			
			if(notimeout):
				scarica_shutdown()		
				stato_rele=False		
				notimeout=False
	
            


    

