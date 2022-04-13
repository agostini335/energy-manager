import threading
from Reading import Reading
import random
import time
import logging
from Modality import Modality

logging.basicConfig(level=logging.DEBUG, handlers=[
        logging.FileHandler("simulation.log"),
        logging.StreamHandler()
    ])

#global variables
last_reading = Reading()
end_program = False
mod = Modality() 

def stream_reader(lock):
    global last_reading,end_program
    while not end_program:
        values = {'r_tensione' : random.randint(0,100),'r_carico' :   random.randint(0,100),'r_produzione' : random.randint(0,100),'r_immissione' : random.randint(0,100),'r_boiler' : random.randint(0,100), 'r_temperatura' :random.randint(0,100)}	
        if lock.acquire(False):
            last_reading.set_values(values)
            lock.release()
        time.sleep(0.1*random.randint(0,10))

def mod_setter(mod_lock):
    global mod,end_program
    while not end_program:
        r = random.randint(0,2)
        if r == 0:
            new_mod = 'OFF'
        elif r == 1:
            new_mod = 'ON'
        else:
            new_mod ='AUTO'
        mod_lock.acquire()
        mod.request_change(new_mod)
        mod_lock.release()
        logging.info("Request change MOD TO: "+new_mod)
        time.sleep(random.randint(3,7))
              
def mod_manager(reading_lock,mod_lock):
    global last_reading,mod,end_program
    while not end_program:
        # check if mod switch should occur
        mod_lock.acquire()
        if mod.to_switch :
           # procedure per il cambio di modalità
           mod.set_current(mod.requested)
           logging.info("Changed MOD TO: "+str(mod.current))
        mod_lock.release() 
        
        if mod.current == 'AUTO':
            reading_lock.acquire()
            current_reading = Reading(values=last_reading.values.copy(),last_update=last_reading.last_update)
            reading_lock.release()
            logging.info("do logic on: "+str(current_reading.values)+" :: reftime "+str(current_reading.last_update))
            time.sleep(1)
        elif mod.current == 'OFF':
            pass
        elif mod.current == 'ON':
            pass

if __name__ == "__main__":
      
    last_reading_lock = threading.Lock()
    mod_lock = threading.Lock()

    # creating threads
    thread_stream_reader = threading.Thread(target=stream_reader, args=(last_reading_lock,))
    thread_mod_setter = threading.Thread(target=mod_setter, args=(mod_lock,))
    thread_mod_manager = threading.Thread(target=mod_manager, args=(last_reading_lock,mod_lock))

    thread_stream_reader.start()
    thread_mod_setter.start()
    thread_mod_manager.start()
 
    try:
        while True:
            pass
    except KeyboardInterrupt:
        end_program=True
    print('END')