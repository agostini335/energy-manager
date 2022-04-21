from DisplayManager import DisplayManager
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)
display_manager = DisplayManager()
import time
i = 0
while True:
    if GPIO.input(10) == GPIO.HIGH:
        print('pressed '+str(i))
        display_manager.driver_print(str(i),1)
        time.sleep(1)
        i +=1


