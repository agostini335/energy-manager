import threading
from Reading import Reading
import random
import time
import logging
from Modality import Modality
from StateMachine import *
from SystemManager import SystemManager

logging.basicConfig(level=logging.DEBUG, handlers=[
        logging.FileHandler("simulation.log"),
        logging.StreamHandler()
    ])

#global variables
last_reading = Reading()
end_program = False
mod = Modality()
system_manager=SystemManager()
state_manager = StateManager(InitState(),system_manager)

def stream_reader(lock):
    global last_reading,end_program
    while not end_program:
        values = {'r_tensione' : random.randint(0,100),'r_carico' :   random.randint(0,100),'r_produzione' : random.randint(0,100),'r_immissione' : random.randint(0,100),'r_boiler' : random.randint(0,100), 'r_temperatura' :random.randint(0,100)}	
        if lock.acquire(False):
            last_reading.set_values(values)
            lock.release()
        time.sleep(2*random.randint(0,10))

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
        #mod.request_change(new_mod)
        mod.request_change('AUTO')
        mod_lock.release()
        #logging.info("Request change MOD TO: "+new_mod)
        time.sleep(random.randint(3,7))
              
def mod_manager(reading_lock,mod_lock):
    global last_reading,mod,end_program
    while not end_program:
        #check if mod switch should occur
        mod_lock.acquire()
        if mod.to_switch :
            #procedure per il cambio di modalita
            mod.set_current(mod.requested)
            logging.info("Changed MOD TO: "+str(mod.current))
        mod_lock.release() 
        
        if mod.current == 'AUTO':
            reading_lock.acquire()
            current_reading = last_reading.get_copy()
            reading_lock.release()
            state_manager.handle_reading(current_reading)
            logging.info("STATE: "+str(state_manager._state.name)+ "now:"+str(datetime.now())+" current reading: "+str(current_reading.last_update) +" fresh: "+str(current_reading.is_fresh))
            time.sleep(1)
        elif mod.current == 'OFF':
            pass
        elif mod.current == 'ON':
            pass

if __name__ == "__main__":
      
    last_reading_lock = threading.Lock()
    mod_lock = threading.Lock()

    #creating threads
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