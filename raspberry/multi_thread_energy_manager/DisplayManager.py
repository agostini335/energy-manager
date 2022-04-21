import lcd_driver
class DisplayManager():
    current_mod=""
    request_mod = ""
    state = ""
    values = {'r_tensione' : 0,'r_carico' :  0,'r_produzione' : 0,'r_immissione' : 0,'r_boiler' : 0, 'r_temperatura' : 0, 'avg_temperatura': 0}


    def print_reading(self):
        d = self.values
        r1="rete: "+str(d['r_tensione']).ljust(4)[:4]+" car: "+str(d['r_carico']).ljust(4)[:4]
        if d['r_immissione']>0:
            r2="prd: "+str(d['r_produzione']).ljust(4)[:4]+" imm: "+str(d['r_immissione']).ljust(4)[:4]
        else:
            r2="prd: "+str(d['r_produzione']).ljust(4)[:4]+" pre: "+str(-1*int(d['r_immissione'])).ljust(4)[:4]

        r3="boi: "+str(d['r_boiler'])+" tmp: "+str(d['avg_temperatura'])
        self.driver_print(r1,1)
        self.driver_print(r2,2)
        self.driver_print(r3,3)


    def print_mod_state(self):
        s = self.current_mod.ljust(5)[:5] +" | "+self.state.ljust(5)[:5]+" | "+self.request_mod.ljust(5)[:5]
        lcd_driver.lcd_string(s,4)
    
    def set_request_mod(self,s):
        self.request_mod =s
        
    def set_current_mod(self,s):
        self.current_mod =s

    def set_state(self,s):
        self.state =s

    def set_reading_values(self,v):
        self.values = v
    def driver_print(self,s,row):
        lcd_driver.lcd_string(s,row)

