import Adafruit_DHT
import RPi.GPIO as GPIO
import time

DHT22_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4

#while True:
#    humidity, temperature = Adafruit_DHT.read_retry(DHT22_SENSOR, DHT_PIN)
#    if humidity is not None and temperature is not None:
#        print("Temp={0:0.1f}*C  Humidity={1:0.1f}%".format(temperature, humidity))
#    else:
#        print("Failed to retrieve data from humidity sensor")
humidity = None
temp = None
def getReading ():
  while True:
        humidity, temp = Adafruit_DHT.read_retry(DHT22_SENSOR,DHT_PIN)
        if humidity is not None and temp is not None:
            print("Temperature: {0:0.1f}C\t Humidity: {1:0.1f}%".format(temp,humidity))
            return temp,humidity
        else:
            print("No sensor reading! Check circuit connections.")
        time.sleep(2)

temp, humidity = getReading()
print(temp)
print(humidity)


