import RPi.GPIO as GPIO
import time
    
    
Moisture_Pin = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(Moisture_Pin, GPIO.IN)
count = 0

def isDry():
    if GPIO.input(Moisture_Pin) == GPIO.HIGH:
      return True
    else:
       return False
    




        

