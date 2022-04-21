from DisplayManager import DisplayManager
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)
display_manager = DisplayManager()
import time
from datetime import datetime
from itertools import cycle

lst = ['AUTO', 'ON', 'OFF']

pool = cycle(lst)

k=2
list
while True:
    if GPIO.input(10) == GPIO.HIGH:
        i = next(pool)
        print('pressed '+i)
        display_manager.driver_print(str(i),1)
        pressed = datetime.now()
        time.sleep(1)
    if pressed-datetime.now()>k:
        display_manager.driver_print("pressed",2)



