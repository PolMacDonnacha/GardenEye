import RPi.GPIO as GPIO
import time
import moisture1

Pump_Relay_Pin = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(Pump_Relay_Pin, GPIO.OUT)

            
def runPump(seconds):
        while moisture1.isDry() == True:
            GPIO.output(Pump_Relay_Pin, 1)
        GPIO.output(Pump_Relay_Pin, 0)
        time.sleep(seconds)

       
def pumpOn():
        GPIO.output(Pump_Relay_Pin, 1)
        
def pumpOff():
        GPIO.output(Pump_Relay_Pin, 0)
     
