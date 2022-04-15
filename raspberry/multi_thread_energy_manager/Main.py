import threading
from Reading import Reading
import random
import time
import logging
from Modality import Modality
from StateMachine import *
from SystemManager import SystemManager

logging.basicConfig(level=logging.DEBUG, handlers=[
        logging.FileHandler("energy_manager.log"),
        logging.StreamHandler()
    ])

last_reading = Reading()
end_program = False
system_manager = SystemManager()


mod = Modality(default='OFF')
if mod.current == 'OFF':
    state_manager = StateManager(OffState(),system_manager)
elif mod.current == 'ON':
    state_manager = StateManager(OnState(),system_manager)
elif mod.current == 'AUTO':
    state_manager = StateManager(InitState(),system_manager)
else:
    raise(" NOT IMPLEMENTED MOD")

def stream_reader(lock):
    global last_reading,end_program,system_manager
    while not end_program:
        if system_manager.ser.in_waiting>0:
            line = system_manager.ser.readline()
            #string conversion
            try:
                line=line[:-2]
                line_split = line.decode().split(';')
				# string type check
                if ( len(line_split) == 7 and line_split[0]=='1' ):
                    values = {'r_tensione' : int(line_split[1]),'r_carico' :   int(line_split[2]),'r_produzione' : int(line_split[3]),'r_immissione' : int(line_split[4]),'r_boiler' : int(line_split[5]), 'r_temperatura' : float(line_split[6])}				
                    if lock.acquire(False):
                        last_reading.set_values(values)
                        lock.release()
                elif ( len(line_split) == 2 and line_split[0]=='0'):
                    #TODO scenario not implemented r_boiler = int(line_split[1])
                    pass
                else:
                    print("invalid string")								
            except:
                print("stream reader error")

def mod_setter(mod_lock):
    #TODO REPLACE WITH BUTTON CODE
    ###################################################################
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
        #logging.info("Request change MOD TO: "+new_mod)
        time.sleep(10*random.randint(0,10))
    ###################################################################

def mod_manager(reading_lock,mod_lock):
    global last_reading,mod,end_program
    while not end_program:
        #mod setting
        old_mod = mod.current
        if mod.set_current(mod.requested):
            #transizone avvenuta
            logging.info("Changing MOD from "+ str(old_mod)+" TO: "+str(mod.current))
            if mod.current == 'AUTO':
                state_manager.transition_to(InitState())                
            elif mod.current == 'OFF':
                state_manager.transition_to(OffState())                
            elif mod.current == 'ON':
                state_manager.transition_to(OnState())
            time.sleep(2)
        if mod_lock.locked():
            mod_lock.release()    
        #handling reading
        reading_lock.acquire()
        current_reading = last_reading.get_copy()
        reading_lock.release()
        state_manager.handle_reading(current_reading)
        if current_reading.is_fresh:
            logging.info("STATE: "+str(state_manager._state.name)+ "now:"+str(datetime.now())+" current reading: "+str(current_reading.last_update) +" fresh: "+str(current_reading.is_fresh))
                



if __name__ == "__main__":
      
    last_reading_lock = threading.Lock()
    mod_lock = threading.Lock()
    mod_lock.acquire() # priority to default modality
    
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