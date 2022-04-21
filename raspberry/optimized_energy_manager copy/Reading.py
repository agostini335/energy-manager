from datetime import datetime
from collections import deque
import logging
import numpy as np

class Reading():
    def __init__(self,values=None,last_update=None,temp_deque_size=30,is_fresh=False):
        self.creation_time=datetime.now()
        self.last_update=last_update
        self.values=values
        self.is_fresh=is_fresh
        self.temp_dequeue = deque([0]*temp_deque_size,maxlen=temp_deque_size) 

    def set_values(self,values):
        self.temp_dequeue.appendleft(values['r_temperatura'])
        values['avg_temperatura'] = np.round(np.mean(self.temp_dequeue),decimals=1)
        self.values = values
        self.last_update = datetime.now()
        logging.info("STREAM: update"+str(values)+"at:"+str(self.last_update))
        self.is_fresh =True
    
    def get_copy(self):
        if self.values == None:
            return Reading(values = {'r_tensione' : 0,'r_carico' :  0,'r_produzione' : 0,'r_immissione' : 0,'r_boiler' : 0, 'r_temperatura' : 0, 'avg_temperatura': 0},last_update=datetime.now(),temp_deque_size=0,is_fresh=False)
        r = Reading(self.values.copy(),self.last_update,temp_deque_size=0,is_fresh=self.is_fresh)
        self.is_fresh = False
        return r

