import Adafruit_DHT
import RPi.GPIO as GPIO
import time
import firebase_admin
from firebase_admin import db
import threading
import json
import pump1
import temp1
import moisture1
import light
import fan1

cred = firebase_admin.credentials.Certificate("/home/pi/Documents/garden-auto-2b24d-firebase-adminsdk-pth24-10f650b13b.json")
firebase_admin.initialize_app(cred, {
    'databaseURL':'https://garden-auto-2b24d-default-rtdb.europe-west1.firebasedatabase.app/'
    })

#DHT_PIN = 4
#Fan_Relay_Pin = 17
#Pump_Relay_Pin = 27
#Moisture_Pin = 18
#Light_Pin = 23
autoPump = True
autoCool = True


GPIO.setmode(GPIO.BCM)
seconds = 3 #change to read from user defined number
count = 0


def startSystem():
    global count,seconds,autoPump,AutoCool
    while True:
        print('AutoPump: ', autoPump)
        count += 1
        temp,humidity = temp1.getReading()
        print(count)
        isDry = moisture1.isDry()

        if isDry is True and autoPump is True:
            pumpThread = threading.Thread(target=pump1.runPump,args=(seconds,))
            pumpThread.start()
        if temp > 23 and autoCool is True:
            fanThread = threading.Thread(target=fan1.runFan,args=(seconds,))
            fanThread.start()
            
        time.sleep(2)

sysThread = threading.Thread(target=startSystem,args=())
sysThread.start()

def autoCoolOn():
    global autoCool
    autoCool = True
    
def autoCoolOff():
    global autoCool
    autoCool = False
    
def autoPumpOn():
    global autoPump
    autoPump = True
    
def autoPumpOff():
    global autoPump
    autoPump = False
    
