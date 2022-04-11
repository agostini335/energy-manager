import threading
from Reading import Reading
import random
import time
from SystemManager import SystemManager

last_reading = Reading()
end_program = False
system_manager = SystemManager()

def stream_reader(lock):
    global last_reading,end_program,system_manager
    while not end_program:
        if system_manager.ser.in_waiting>0:
            line = system_manager.readline()
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
                
def do_logic(lock):
    global last_reading
    lock.acquire()
    values = last_reading.values
    upd = last_reading.last_update
    lock.release()
    print("letto "+str(values)+" at "+str(upd))
    time.sleep(10)


if __name__ == "__main__":
      
    last_reading_lock = threading.Lock()

    # creating threads
    thread_stream_reader = threading.Thread(target=stream_reader, args=(last_reading_lock,))
      
    # start stream thread
    thread_stream_reader.start()
     
    try:
        while True:
            thread_do_logic = threading.Thread(target=do_logic, args=(last_reading_lock,))
            thread_do_logic.start()
            thread_do_logic.join()

    except KeyboardInterrupt:
        pass
    end_program=True
    print('END')