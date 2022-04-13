class Modality():
    def __init__(self):
        self.implemented_mods = ['OFF','ON','AUTO']
        self.requested = 'OFF'
        self.current = 'OFF'
        self.to_switch = False
    def request_change(self,mod):
        if mod in self.implemented_mods:
            self.requested = mod
            if self.requested != self.current:
                self.to_switch = True
        else:
            raise("not implemented")
    def set_current(self,mod):
        if mod in self.implemented_mods:
            self.current = mod
            self.to_switch = False
        else:
            raise("not implemented")

