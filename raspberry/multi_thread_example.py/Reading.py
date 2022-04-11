from datetime import datetime
class Reading():
    def __init__(self) -> None:
        self.creation_time=datetime.now()
        self.last_update=datetime.now()
        self.values=None
    def set_values(self,values):
        self.values = values
        self.last_update = datetime.now()
        print(self.last_update)
