import time
import datetime
import os
from firebase_admin import db
import pyrebase
import configfile

#Pyrebase is a popular wrapper for the Firebase API developed by 13 contributors on github
# https://github.com/thisbejim/Pyrebase
firebase = pyrebase.initialize_app(configfile.firebaseConfig)
storage = firebase.storage()

def countFiles(directory):
    print('Counting files')
    count = len(os.listdir(directory))
    return count

def deleteFiles(directory):
    print(f'Deleting files from {directory}')
    os.system(f'rm {directory}')

def getAvailableSpace():
    statvfs = os.statvfs(".")
    available_megabytes = statvfs.f_frsize * statvfs.f_bavail/ 1000000 #Number of megabytes free
    return available_megabytes
        
def appendToLog(file,message):
    with open(f'{file}.txt',"a") as log_file:
        log_file.write(f"{getTime()}: {message}\n")
        
def appendToCsv(file,message):
    with open(f'{file}.csv',"a") as csv_file:
        csv_file.write(message)
 
def getTime():
    currentTime= datetime.datetime.now()
    formattedTime = currentTime.strftime("%Y-%m-%d_%H:%M:%S")
    return formattedTime

def updateDb(ref,values):
    try:
        db_ref = db.reference(f"PiDevices/{os.environ['Device']}{ref}")
        db_ref.update(values)
    except Exception as e:
        errorMessage = f"{getTime()}: Database Update Error: {e}\n"
        appendToLog("error",errorMessage)

def readDb(ref):
    try:
        #print('Reading from database')
        #print(f"PiDevices/{os.environ['Device']}{ref}")
        db_ref = db.reference(f'PiDevices/{os.environ["Device"]}{ref}')#Point towards the database section passed in as a reference

        items = db_ref.get()#Retrieve all of the data in the database reference
        os.environ['usingBackupData'] = 'false'
        #print(items)
        return items
    except Exception as e:
        print('Failed to read database, using backup data')
        errorMessage = f"{getTime()}: Database Read Error: {e}\n"
        appendToLog("error",errorMessage)
        os.environ['usingBackupData'] = 'true'
        backupItems = {}
        backupItems['autoCool'] = 1
        backupItems['autoPump'] = 1
        backupItems['autoTimelapse'] = 0
        backupItems['timelapseFps'] = 40
        backupItems['timelapseInterval'] = 86400
        backupItems['timelapseSwitch'] = 0
        backupItems['timelapseLength'] = 43800
        backupItems['fanSwitch'] = 0
        backupItems['fanTime'] = 60
        backupItems['maxTemp'] = 30
        backupItems['pumpSwitch'] = 0
        backupItems['pumpTime'] = 120
        backupItems['refreshInterval'] = 3
        backupItems['idealSoilMoisture'] = 40
        os.environ['TimelapseKeepAlive'] = 'True'
        os.environ['TimelapseRunning'] = 'False'
        appendToLog("error","Returning backup data")
        return backupItems
        
def pushToStorage(firebaseFile,localFile):
    storage.child(firebaseFile).put(localFile)

def getEnvStats():
    return f"{getTime()}\nTemp: {os.environ['Temperature']}C\nHumidity: {os.environ['Humidity']}\nSoil Moisture: {os.environ['soilMoisture']}\nLight: {os.environ['light']}% \nPump: {os.environ['Pump']}\nFan: {os.environ['Fan']}"

