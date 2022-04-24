from multiprocessing import Process, Queue
import random
import pandas as pd
import datetime
import time 
from datetime import date
import os

def rand_num(queue):
    while 1:
        today = date.today()
        # Month abbreviation, day and year	
        d4 = today.strftime("%b-%d-%Y")
        df = pd.DataFrame([queue.get()]) 
        if not os.path.isfile(d4+".csv",):
            df.to_csv(d4+".csv", header='column_names')
        else: # else it exists so append without writing the header
            df.to_csv(d4+".csv", mode='a', header=False)

if __name__ == "__main__":
    queue = Queue()
    process = Process(target=rand_num, args=(queue,))
    process.start()

    while 1:
        queue.put({'r_tensione' : random.randint(0,100),'r_carico' :   random.randint(0,100),'r_produzione' : random.randint(0,100),'r_immissione' : random.randint(0,600),'r_boiler' : random.randint(0,3000), 'r_temperatura' :random.randint(0,100), 'tmp':datetime.datetime.now()}	)
        time.sleep(2)



