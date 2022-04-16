#!/usr/bin/python
import spidev
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

#Open SPI bus
spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz=1000000
voltageRef = 3.3
bitRes = 12
CS_ADC = 8
GPIO.setup(CS_ADC, GPIO.OUT)

# Read SPI data from 12-bit MCP3208 chip
# Channel must be an integer 0-7

#80 was [0, 12, 213] at 3.3vRef
#80 was [0, 12, 228] at 5vRef
# 80% example adc bytes: 00000000 00001100 11100100
# 80% example
def ReadChannel3208(channel):
  #SOURCED FROM ARDUITRONICS, THEY SELL THIS CHIP: https://www.arduitronics.com/article/53/raspberry-pi-analog-input-with-adc-mcp3208
  # '|' Uses the bit if it appears as '1' on either side of the operand
  # e.g. 3|6 (00000011|00000110) = 00000111
  adc = spi.xfer2([4|2|(channel>>2),(channel&2)<<6,0]) #0000011x,xx000000,00000000
  # '&' Uses the bit if it appears as '1' on both sides of the operand
  # e.e. 3|6 (00000011|00000110) = 00000010
  data = ((adc[1]&15) << 8) + adc[2]
  return data

def ConvertToVoltage(value, vref):
  return vref*(value/(2**bitRes-1))

def getPercentage(channel):
  GPIO.output(CS_ADC, GPIO.LOW)
  value = ReadChannel3208(channel)
  GPIO.output(CS_ADC, GPIO.HIGH)
  voltage = ConvertToVoltage(value, voltageRef) 
  percentage = int((voltage/voltageRef)*100)
  return percentage

def getTemperature(channel):
  GPIO.output(CS_ADC, GPIO.LOW)
  value = ReadChannel3208(channel)
  GPIO.output(CS_ADC, GPIO.HIGH)
  voltage = ConvertToVoltage(value, voltageRef) 
  temperature = float((voltage-0.5)*100)
  #print(f"Temp: {temperature}")
  return voltage
