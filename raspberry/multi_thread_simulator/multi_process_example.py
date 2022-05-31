from multiprocessing import Process, Queue
import random
import pandas as pd
import datetime
import time 
from datetime import date
import os
import csv



def saver(queue,path="", buffer_size = 5):
    df = pd.DataFrame()
    while 1:
        today = date.today()
        file_name = today.strftime("%b-%d-%Y") +".csv"
        full_name = path+file_name

        df = df.append([queue.get()],ignore_index=True) 

        if len(df) >= buffer_size:
            if not os.path.isfile(full_name,):
                df.to_csv(full_name, header='column_names')
            else: # else it exists so append without writing the header
                df.to_csv(full_name, mode='a', header=False)
            df = df[0:0]
            
def simplesaver(queue,path="", buffer_size = 5):
    write_list = []
    fieldnames = ['r_tensione','r_carico','r_produzione','r_immissione','r_boiler','r_temperatura','tmp']
    while 1:
        today = date.today()
        file_name = today.strftime("%b-%d-%Y") +".csv"
        full_name = path+file_name

        write_list.append(queue.get())

        if len(write_list) >= buffer_size:
            if not os.path.isfile(full_name):
                with open(full_name, 'w', encoding='ASCII', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(write_list)               
            else: # else it exists so append without writing the header
                with open(full_name, 'a', encoding='ASCII', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writerows(write_list)
            write_list = []


if __name__ == "__main__":
    queue = Queue()
    process = Process(target=simplesaver, args=(queue,))
    process.start()

    while 1:
        queue.put({'r_tensione' : random.randint(0,100),'r_carico' :   random.randint(0,100),'r_produzione' : random.randint(0,100),'r_immissione' : random.randint(0,600),'r_boiler' : random.randint(0,3000), 'r_temperatura' :random.randint(0,100), 'tmp':datetime.datetime.now()}	)
        time.sleep(2)



