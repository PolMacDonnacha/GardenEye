import RPi.GPIO as GPIO
import time
import moisture
import os
import utility

Pump_Relay_Pin = 27
GPIO.setmode(GPIO.BCM)
GPIO.setup(Pump_Relay_Pin, GPIO.OUT)
os.environ['Pump'] = 'Inactive'#Initialize

#while moisture1.isDry() == True:            
def runPump(seconds): 
    GPIO.output(Pump_Relay_Pin, 1)
    os.environ['Pump'] = 'Active'#Note pump is active: used in annotating pictures
    os.environ['WateredTime'] = f'{utility.getTime()}'
    time.sleep(seconds)
    GPIO.output(Pump_Relay_Pin, 0)
    os.environ['Pump'] = 'Inactive'#Note pump is inactive: used in annotating pictures

def pumpOn():
    GPIO.output(Pump_Relay_Pin, 1)
    os.environ['WateredTime'] = f'{utility.getTime()}'
    os.environ['Pump'] = 'Active'#Note pump is active: used in annotating pictures
    
def pumpOff():
    GPIO.output(Pump_Relay_Pin, 0)
    os.environ['Pump'] = 'Inactive'#Note pump is inactive: used in annotating pictures

     
