from flask import Flask
import pump1
import fan1
import gardeneye

app = Flask(__name__)
@app.route('/')
def appStart():
    return 'GardenEye is running!.'

@app.route('/pump/on')
def pumpOn():
    pump1.pumpOn()
    return 'Turning on the pump.'

@app.route('/pump/off')
def pumpOff():
    pump1.pumpOff()
    return 'Turning off the pump.'

@app.route('/pump/auto/on')
def pumpAutoOn():
    gardeneye.autoPumpOn()
    return 'Pump will toggle automatically.'

@app.route('/pump/auto/off')
def pumpAutoOff():
    gardeneye.autoPumpOff()
    return 'Pump will not toggle automatically.'

@app.route('/fan/on')
def fanOn():
    fan1.fanOn()
    return 'Turning on the fan.'

@app.route('/fan/off')
def fanOff():
    fan1.fanOff()
    return 'Turning off the fan.'

@app.route('/fan/auto/on')
def fanAutoOn():
    gardeneye.autoCoolOn()
    return 'Fan will toggle automatically.'

@app.route('/fan/auto/off')
def fanAutoOff():
    gardeneye.autoCoolOff()
    return 'Fan will not toggle automatically.'



