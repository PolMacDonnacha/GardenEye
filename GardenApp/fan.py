import RPi.GPIO as GPIO
import time
import os

Fan_Relay_Pin = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(Fan_Relay_Pin, GPIO.OUT)
os.environ['Fan'] = 'Inactive'#Initialize

           
def runFan(seconds):
    GPIO.output(Fan_Relay_Pin, 1)
    os.environ['Fan'] = 'Active'#Note fan is active: used in annotating pictures
    time.sleep(seconds)
    GPIO.output(Fan_Relay_Pin, 0)
    os.environ['Fan'] = 'Inactive'#Note fan is inactive: used in annotating pictures
       
def fanOn():
    GPIO.output(Fan_Relay_Pin, 1)
    os.environ['Fan'] = 'Active'#Note fan is active: used in annotating pictures
    
def fanOff():
    GPIO.output(Fan_Relay_Pin, 0)
    os.environ['Fan'] = 'Inactive'#Note fan is inactive: used in annotating pictures
    
