import RPi.GPIO as GPIO
import time
import utility
import os
import adc

Light_ADC_Channel = 4
GPIO.setmode(GPIO.BCM)

def measureLight():
    try:    
        light = adc.getPercentage(Light_ADC_Channel)
        print(f"Light: {light}%\n")
        os.environ['light'] = f"{light}"#Set the Light level: used in annotating pictures
        utility.appendToCsv("light",f"{utility.getTime()},{light}\n")
        return light
    except Exception as e:
        print(f'measureLight except block reached: {e}\n')
        errorMessage = f"{utility.getTime()}: measureLight Function Error: {e}\n"
        utility.appendToLog("error",errorMessage)

#measureLight()