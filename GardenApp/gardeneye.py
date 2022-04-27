import RPi.GPIO as GPIO
import time
import firebase_admin
from firebase_admin import credentials
import threading
import json
import pump
import temp
import moisture
import light
import fan
import camera
import configfile
import utility
import os
#import requests
#from requests.packages import urllib3

firebase_admin.initialize_app(configfile.cred, configfile.firebaseConfig)

#DHT_PIN = 22
#soil_Temp_Pin = 4
#Fan_Relay_Pin = 17
#Pump_Relay_Pin = 27
#Moisture_Pin = 18
#Light_Pin = 23
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
timelapseRunning = 0
lock = threading.Lock()


def timelapseStart(timelapseLength,timelapseFps,timelapseInterval):
    print('Creating timelapse thread')
    timelapseThread = threading.Thread(target=camera.startTimelapse,args=(timelapseLength,timelapseFps,timelapseInterval,))
    os.environ['TimelapseRunning'] = 'True'#Set the timelapse status as running
    os.environ['TimelapseKeepAlive'] = 'True'#This line keeps the timelapse running, if the user wants to end a timelapse early, this is set to False
    print('Timelapse thread created')
    utility.appendToLog("thread","Starting timelapse thread")
    timelapseThread.start()#start the timelapse thread
    
def startSystem():
    os.environ['TimelapseRunning'] = 'False'
    print('starting')
    liveThread = threading.Thread(target=camera.liveViewCapture,args=())#Start the live view of plants
    utility.appendToLog("thread","Starting live view thread")
    liveThread.start()
    while True:
        try:
            controlItems = utility.readDb('/control/')
            autoCool = controlItems['autoCool']
            autoPump = controlItems['autoPump']
            autoTimelapse = controlItems['autoTimelapse']
            timelapseFps = controlItems['timelapseFps']
            timelapseInterval = controlItems['timelapseInterval']
            timelapseSwitch = controlItems['timelapseSwitch']
            timelapseLength = controlItems['timelapseLength']
            fanSwitch = controlItems['fanSwitch']
            fanTime = controlItems['fanTime']
            maxTemp = controlItems['maxTemp']
            pumpSwitch = controlItems['pumpSwitch']
            pumpTime = controlItems['pumpTime']
            refreshInterval = controlItems['refreshInterval']
            idealSoilMoisture = controlItems['idealSoilMoisture']
            #print('autoCool: ', autoCool)
            #print('autoPump: ', autoPump)
            #print('autoTimelapse: ', autoTimelapse)
            #print('timelapseSwitch: ', timelapseSwitch)
            #print('timelapseInterval: ', timelapseInterval)
            #print('timelapseFps: ', timelapseFps)
            print(f"TimelapseRunning: {os.environ['TimelapseRunning']}")
            #print('timelapseLength: ', timelapseLength)
            #print('fanSwitch: ', fanSwitch)
            #print('fanTime: ', fanTime)
            #print('maxTemp: ', maxTemp)
            #print('pumpSwitch: ', pumpSwitch)
            #print('pumpTime: ', pumpTime)
            print(f"liveThread.isAlive(): {liveThread.isAlive()}")
           # if not liveThread.isAlive():
           #     utility.appendToLog("thread","Starting live view thread")
           #     liveThread.join()
           #     liveThread.start()#Restart the live view of plants
                
            #temperature,humidity = temp.getReading()
            if os.environ['DHT'] != 'Active':
                tempThread = threading.Thread(target=temp.getReading,args=())
                tempThread.start()
                
            #isDry = moisture.isDry()
            soilMoisture = moisture.getSoilMoisture()
            lightLevel = light.measureLight()
            
            if soilMoisture < idealSoilMoisture and autoPump is 1 and os.environ['Pump'] != 'Active':
                pumpThread = threading.Thread(target=pump.runPump,args=(pumpTime,))
                utility.appendToLog("thread","Starting pump thread")
                pumpThread.start()
            # If automatic controls are off, check switch columns
            elif autoPump is 0: 
                if pumpSwitch is 1:
                    print('Activating pump')
                    pump.pumpOn()
                else:
                    pump.pumpOff()
            
            if float(os.environ['Temperature']) > maxTemp and autoCool is 1 and os.environ['Fan'] != 'Active':
                fanThread = threading.Thread(target=fan.runFan,args=(fanTime,))
                utility.appendToLog("thread","Starting fan thread")
                fanThread.start()
            elif autoCool is 0:
                if fanSwitch is 1:
                    print('Activating fan')
                    fan.fanOn()
                else:
                    fan.fanOff()
                    
            timelapseActive = os.environ['TimelapseRunning']
            if autoTimelapse is 1 and timelapseActive == 'False': #If the timelapse isn't running and set to automatic
                timelapseStart(timelapseLength,timelapseFps,timelapseInterval)
            else: # autoTimelapse is 0
                if timelapseSwitch is 1 and timelapseActive == 'False':#Start timelapse if it is off
                    os.environ['TimelapseRunning'] = 'True'
                    print(f"TimelapseRunning: {os.environ['TimelapseRunning']}")
                    print('Timelapse will be started')
                    timelapseStart(timelapseLength,timelapseFps,timelapseInterval)
                    
                elif timelapseSwitch is 0 and timelapseActive == 'True':#Stop timelapse if it is on
                    print('Setting keepAlive to false')
                    os.environ['TimelapseKeepAlive'] = 'False'# 0 stops the timelapse
                    os.environ['TimelapseRunning'] = 'False'#Set the timelapse status as not running     
            if os.environ['usingBackupData'] == 'false':
                lock.acquire()
                utility.updateDb("/",{'plot/temperature': float(os.environ['Temperature']),'plot/humidity': float(os.environ['Humidity']), 'plot/soilMoisture': soilMoisture, 'plot/lightLevel': lightLevel, 'plot/timeWatered': os.environ['WateredTime']})
                lock.release()
            time.sleep(refreshInterval)
        except Exception as e:
            print(f'Catch block reached: {e}')
            errorMessage = f"Master Function Error: {e}"
            utility.appendToLog("error",errorMessage)
            pump.pumpOff()
            fan.fanOff()
            os.environ['TimelapseRunning'] = 'False'

def main():
    #plotItems = utility.readDb("/plot")["timeWatered"]#Initialize
    #print(f"Plot items: {plotItems}")
    os.environ['WateredTime'] =utility.readDb("/plot")["timeWatered"]#Initialize
    sysThread = threading.Thread(target=startSystem,args=())#Start the system
    utility.appendToLog("thread","Starting main thread")
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
    
