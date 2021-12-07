import RPi.GPIO as GPIO
import time

Light_Pin = 23
GPIO.setmode(GPIO.BCM)
GPIO.setup(Light_Pin, GPIO.IN)

#def measureLight():
    
