import RPi.GPIO as GPIO
import time

Fan_Relay_Pin = 27
GPIO.setmode(GPIO.BCM)
GPIO.setup(Fan_Relay_Pin, GPIO.OUT)

           
def runFan(seconds):
        GPIO.output(Fan_Relay_Pin, 1)
        time.sleep(seconds)
        GPIO.output(Fan_Relay_Pin, 0)

       
def fanOn():
        GPIO.output(Fan_Relay_Pin, 1)
        
def fanOff():
        GPIO.output(Fan_Relay_Pin, 0)
        