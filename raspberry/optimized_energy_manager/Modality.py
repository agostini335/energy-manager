class Modality():
    def __init__(self,default='OFF'):
        self.implemented_mods = ['OFF','ON','AUTO']
        self.requested = default
        self.current = default
        self.to_switch = True

    def request_change(self,mod):
        if mod in self.implemented_mods:
            self.requested = mod
            self.to_switch=True
        else:
            raise("not implemented")
    
    def set_current(self,mod):
        if mod in self.implemented_mods:
            if mod!= self.current:
                self.current=mod            
                return True
            return False
        else:
            raise("not implemented")

