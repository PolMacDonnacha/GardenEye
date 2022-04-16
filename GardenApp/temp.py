import Adafruit_DHT
import RPi.GPIO as GPIO
import time
import os
import utility

DHT22_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 22
soilTempPin = 4
os.environ['Temperature'] = '0'#Initialize
os.environ['Humidity'] = '0'#Initialize
os.environ['DHT'] = 'Inactive'#Initialize


def getReading ():
  while True:
        os.environ['DHT'] = 'Active'#Prevents multiple identical threads
        humidity, temp = Adafruit_DHT.read_retry(DHT22_SENSOR,DHT_PIN)
        if humidity is not None and humidity <= 100 and temp is not None:
            print("Temperature: {0:0.1f}C\t Humidity: {1:0}%\n".format(temp,round(humidity)))
            os.environ['Temperature'] = f'{float(round(temp))}'#Set the temperature: used in annotating pictures
            os.environ['Humidity'] = f'{float(round(humidity))}'#Set the humidity: used in annotating pictures
            utility.appendToCsv("temp_humid",f"{utility.getTime()},{round(temp)},{round(humidity)}\n")
            os.environ['DHT'] = 'Inactive'
            return #float(round(temp,1)),float(round(humidity))
        else:
            print("Failed to retrieve data from humidity sensor! Check circuit connections.")
            os.environ['DHT'] = 'Inactive'
            utility.appendToLog("error","Failed to retrieve data from humidity sensor! Check circuit connections.")
        #time.sleep(2)




