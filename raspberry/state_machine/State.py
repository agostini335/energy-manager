from datetime import datetime

class AbstractState():
    def __init__(self,context):
        self._context = context
        self.start_time = datetime.now()
    def on_new_read(self,valid,r_carico,r_produzione,r_immissione,r_boiler,r_temperatura,avg_temperatura):
        assert(False)
    def on_start(self):
        assert(False)
    def on_exit(self):
        assert(False)


class TimeoutState(AbstractState):
    def __init__(self,context):
        super.__init__(context)
        self.name="TimeoutState"
    def on_start(self):
        SF.rele_triac_off()
    def on_new_read(self,valid,r_carico,r_produzione,r_immissione,r_boiler,r_temperatura,avg_temperatura):
        if valid:
            self.context.transition_to(ActiveState())
    def on_exit(self):
        pass

class ActiveState(AbstractState):
    def __init__(self,context):
        super.__init__(context)
        self.name="State"
    def on_start(self):
        SF.rele_triac_on()
    def on_new_read(self, valid, r_carico, r_produzione, r_immissione, r_boiler, r_temperatura, avg_temperatura):
        

