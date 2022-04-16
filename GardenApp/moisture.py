import RPi.GPIO as GPIO
import time
import adc
import utility
import os

    
    
Moisture_Pin = 18
Moisture_ADC_Channel = 0
GPIO.setmode(GPIO.BCM)
GPIO.setup(Moisture_Pin, GPIO.IN)
os.environ['soilMoisture'] = 'Not read yet'#Initialize

def getSoilMoisture():
    try:    
        soilMoisture = adc.getPercentage(Moisture_ADC_Channel)
        print(f"Soil moisture: {soilMoisture}%\n")
        os.environ['soilMoisture'] = f'{soilMoisture}%'#Set the soil moisture: used in annotating pictures
        utility.appendToCsv("moisture",f"{utility.getTime()},{soilMoisture}\n")
        return soilMoisture
    except Exception as e:
        print(f'getSoilMoisture except block reached: {e}\n')
        errorMessage = f"{utility.getTime()}: getSoilMoisture Function Error: {e}\n"
        utility.appendToLog("error",errorMessage)

#Digital version
def isDry():
    if GPIO.input(Moisture_Pin) == GPIO.HIGH:
      return True
    else:
       return False
    
    




        

