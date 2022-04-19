import lcd_driver
class DisplayManager():
    current_mod=""
    request_mod = ""
    state = ""

    def show_reading(self,d):
        r1="rete: "+str(d['r_tensione'])+" car: "+str(d['r_carico'])
        if d['r_immissione']>0:
            r2="prd: "+str(d['r_produzione'])+" imm: "+str(d['r_immissione'])
        else:
            r2="prd: "+str(d['r_produzione'])+" pre: "+str(-1*int(d['r_immissione']))

        r3="boi: "+str(d['r_boiler'])+" tmp: "+str(d['r_temperatura'])
        self.driver_print(r1,1)
        self.driver_print(r2,2)
        self.driver_print(r3,3)


    def print_mod_state(self):
        s = self.current_mod.ljust(5)[:5] +" "+self.state.ljust(5)[:5]+" "+self.request_mod.ljust(5)[:5]
        lcd_driver.lcd_string(s,4)
    
    def print_request_mod(self,s):
        self.request_mod =s
        self.print_mod_state()

    def print_current_mod(self,s):
        self.current_mod =s
        self.print_mod_state()

    def print_state(self,s):
        self.state =s
        self.print_mod_state()

    def driver_print(self,s,row):
        # in real system
        lcd_driver.lcd_string(s,row)

