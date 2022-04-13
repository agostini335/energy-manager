from datetime import datetime
from collections import deque
import logging
import numpy as np

class Reading():
    def __init__(self,values=None,last_update=None,temp_deque_size=30):
        self.creation_time=datetime.now()
        self.last_update=last_update
        self.values=values
        self.temp_dequeue = deque([0]*temp_deque_size,maxlen=temp_deque_size) 
    def set_values(self,values):
        self.temp_dequeue.appendleft(values['r_temperatura'])
        values['avg_temperatura'] = np.around(np.mean(self.temp_dequeue),decimals=1)
        self.values = values
        self.last_update = datetime.now()
        logging.info("reading update"+str(values)+"at:"+str(self.last_update))

