import datetime
import logging
from datetime import datetime
from collections import deque

from nbformat import read


class StateManager():
    _state = None
    system_manager = None
    trace_list = []

    def __init__(self, state, system_manager, trace_max_len=10):

        self.trace_deque = deque(maxlen=trace_max_len)
        self.system_manager = system_manager
        self.transition_to(state)

    def transition_to(self, state):
        if self._state != None:
            logging.info("TRX: from "+self._state.name+" to "+state.name)
        self.trace_deque.appendleft((state.name, datetime.now()))
        logging.info(self.trace_deque)
        self._state = state
        self._state.state_manager = self
        self._state.on_start()

    def handle_reading(self, reading):
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
        self.starting_time = datetime.now()

    def on_exit(self):
        pass

    def handle(self, reading):
        # check the timeout
        if (datetime.now()-self.starting_time).total_seconds() > self.state_manager.system_manager.INIT_MAX_WAITING_TIME:
            self.state_manager.transition_to(TimeOutState())
            return
        # check if it is fresh
        if reading.is_fresh:
            self.readings.append(reading)
        if len(self.readings) >= self.state_manager.system_manager.INIT_MIN_FRESH_READINGS:
            if reading.values['avg_temperatura'] >= self.state_manager.system_manager.TEMP_GOAL:
                self.state_manager.transition_to(TempReachedState())
            else:
                self.state_manager.transition_to(ActiveState())


class TempReachedState(AbstractState):
    def __init__(self):
        self.name = 'TempReachedState'

    def on_start(self):
        self.state_manager.system_manager.scarica_shutdown()

    def on_exit(self):
        pass

    def handle(self, reading):
        if (datetime.now()-reading.last_update).total_seconds() > self.state_manager.system_manager.TEMPREACHED_WAITING_TIME_TO:
            self.state_manager.transition_to(TimeOutState())
            return
        if reading.values['avg_temperatura'] <= (self.state_manager.system_manager.TEMP_GOAL - self.state_manager.system_manager.TEMPREACHED_HISTERESYS):
            self.state_manager.transition_to(ActiveState())


class ActiveState(AbstractState):
    def __init__(self):
        self.name = 'ActiveState'

    def on_start(self):
        self.last_immissione_ok_tmp = None

    def on_exit(self):
        pass

    def handle(self, reading):
        # timeout check
        if (datetime.now()-reading.last_update).total_seconds() > self.state_manager.system_manager.ACTIVE_WAITING_TIME_TO:
            self.state_manager.transition_to(TimeOutState())
            return
        # fresh read check
        if not reading.is_fresh:
            return
        # tempreached check
        if reading.values['avg_temperatura'] >= self.state_manager.system_manager.TEMP_GOAL:
            self.state_manager.transition_to(TempReachedState())
            return

        # immissione check
        if reading.values['r_immissione'] < self.state_manager.system_manager.ACTIVE_MIN_IMMISSIONE:
            if self.last_immissione_ok_tmp == None or (reading.last_update - self.last_immissione_ok_tmp).total_seconds() > self.state_manager.system_manager.ACTIVE_MIN_IMMISSIONE_TO:
                logging.info("ACTIVE STATE: NO IMMISSIONE")
                self.state_manager.system_manager.scarica_shutdown()
            return
        else:
            self.last_immissione_ok_tmp = reading.last_update

        #### CONTROLLER LOGIC ####
        self.state_manager.system_manager.releon()

        if reading.values['r_boiler'] >= self.state_manager.system_manager.ACTIVE_LIMITE_TRIAC \
            or (reading.values['r_immissione'] < self.state_manager.system_manager.ACTIVE_LOWERBOUND_IMM \
                and reading.values['r_boiler'] >= self.state_manager.system_manager.ACTIVE_NOISE_BOILER):
            self.state_manager.system_manager.s_down()
        elif reading.values['r_boiler']> self.state_manager.system_manager.ACTIVE_LIMITE_TRIAC-self.state_manager.system_manager.ACTIVE_DELTA_MAX_TRIAC_UP    \
            and reading.values['r_boiler'] < self.state_manager.system_manager.ACTIVE_LIMITE_TRIAC:
            logging.info("ACTIVE STATE: FASCIA GOAL -> BOILER")
        elif reading.values['r_immissione'] >= self.state_manager.system_manager.ACTIVE_LOWERBOUND_IMM \
            and   reading.values['r_immissione'] <= self.state_manager.system_manager.ACTIVE_UPPERBOUND_IMM:
            logging.info("ACTIVE STATE: FASCIA GOAL -> IMMISSIONE")
        else:        
            self.state_manager.system_manager.s_up()


class TimeOutState(AbstractState):
    def __init__(self):
        self.name = 'TimeOutState'
        self.last_fresh_ts = 0

    def on_start(self):
        self.state_manager.system_manager.scarica_shutdown()

    def on_exit(self):
        pass

    def handle(self, reading):
        if reading.is_fresh and self.last_fresh_ts == 0:
            self.last_fresh_ts = reading.last_update
        elif reading.is_fresh:
            if (reading.last_update-self.last_fresh_ts).total_seconds() < self.state_manager.system_manager.TIMEOUT_TIME_BTWN_FRESH:
                if reading.values['avg_temperatura'] >= self.state_manager.system_manager.TEMP_GOAL:
                    self.state_manager.transition_to(TempReachedState())
                else:
                    self.state_manager.transition_to(ActiveState())
            else:
                self.last_fresh_ts = reading.last_update
