import datetime
import logging
from datetime import datetime
from collections import deque

class StateManager():
    _state = None
    system_manager = None
    trace_list = []

    def __init__(self, state, system_manager,trace_max_len=10**3):
        
        self.trace_deque = deque(maxlen=trace_max_len)
        self.system_manager = system_manager
        self.transition_to(state)
        

    def transition_to(self, state):
        if self._state != None:
            logging.info("TRX: from "+self._state.name+" to "+state.name)
        self.trace_deque.appendleft((state.name,datetime.now()))
        self._state = state
        self._state.state_manager = self
        self._state.on_start()

    def handle_reading(self,reading):
        self._state.handle(reading)



class AbstractState():
    state_manager = None
    name = None
    def on_start():
        pass
    def on_exit():
        pass
    def handle(self):
        pass

class InitState(AbstractState):
    def __init__(self):
        self.name = 'InitState'
        self.readings = []

    def on_start(self):
        self.waiting_reading = self.state_manager.system_manager.INIT_MAX_WAITING_TIME
        self.max_waiting_time = self.state_manager.system_manager.INIT_MIN_FRESH_READINGS
        self.starting_time = datetime.now()
    
    def on_exit(self):
        pass

    def handle(self,reading):
        # check the timeout
        if (datetime.now()-self.starting_time).total_seconds()>self.max_waiting_time:
            self.state_manager.transition_to(TimeOutState())
            return
        #check if it is fresh
        if reading.is_fresh:
            self.readings.append(reading)
        if len(self.readings)>=self.waiting_reading:
            if reading.values['avg_temperatura']>=self.state_manager.system_manager.TEMP_GOAL:
                self.state_manager.transition_to(TempReachedState())
            else:
                self.state_manager.transition_to(ActiveState())

                    
class TempReachedState():
    def __init__(self,waiting_reading=10, max_waiting_time=10):
        self.name = 'TimeOutState'
        
    def on_start(self):
        pass
    
    def on_exit(self):
        pass

    def handle(self,reading):
        pass
class ActiveState():
    def __init__(self,waiting_reading=5, max_waiting_time=20):
        self.name = 'ActiveState'

    def on_start(self):
        pass
    
    def on_exit(self):
        pass

    def handle(self,reading):
        pass
class TimeOutState(AbstractState):
    def __init__(self,waiting_reading=10, max_waiting_time=10):
        self.name = 'TimeOutState'
        self.last_fresh_ts = 0
    def on_start(self):
        self.state_manager.system_manager.scarica_shutdown()

    def on_exit(self):
        pass

    def handle(self,reading):
        if reading.is_fresh and self.last_fresh_ts==0:
            self.last_fresh_ts=reading.last_update
        elif reading.is_fresh:
            if (reading.last_update-self.last_fresh_ts).total_seconds() <self.state_manager.system_manager.TIMEOUT_TIME_BTWN_FRESH:
                self.state_manager.transition_to(ActiveState())
            else:
                self.last_fresh_ts=reading.last_update
            

