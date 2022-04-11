from glob import glob
import threading
from Reading import Reading
import random
import time

last_reading = Reading()
end_program = False

def stream_reader(lock):
    global last_reading,end_program
    while not end_program:
        r = random.randint(0,10)
        if r>3:
            if lock.acquire(False):
                last_reading.set_values(r)
                lock.release()
                
def do_logic(lock):
    global last_reading
    lock.acquire()
    values = last_reading.values
    upd = last_reading.last_update
    lock.release()
    print("letto "+str(values)+" at "+str(upd))
    time.sleep(0.0001)


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