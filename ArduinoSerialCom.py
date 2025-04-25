# WaveShapePlay
# For a detailed YouTube tutorial visit: https://youtu.be/T-s-2tBUfLM

# The other side of this is ArduinoCharInput.ino
# The current time request has not been written yet.
# Arduino Nano with SY-018 Photoresister Sensor Module attached
# A2 to sensor pin marked S, 5V+ to sensor center pin, 
# Gnd to sensor pin marked -

import serial
import time
import configparser
import os

# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the full path to the file in the script's directory
file_path = os.path.join(current_dir, 'dataFile.txt')

# Open the file
dataFile = open(file_path, 'w')

# Read INI file NOTE: I changed this from the WaveShapePlay original INI read routine
# to use the configparser module. 
config = configparser.ConfigParser()
ini_path = os.path.join(current_dir, 'dataSetup.ini')
config.read(ini_path)
numRowsCollect = int(config['Settings']['numRowsCollect'])
numPoints = int(config['Settings']['numPoints'])

ser = serial.Serial('COM12', baudrate=9600, timeout=1)
time.sleep(3)

# dataFile = open('C:/Users/maryf/OneDrive/Documents/dataFile.txt', 'w')
dataList = [0] * numPoints

print('Connected to: ' + ser.portstr) 
print('Collecting ' + str(numPoints) + ' data points for ' + str(numRowsCollect) + ' rows.')    

def getValues():
    ser.write(b'g')
    arduinoData = ser.readline().decode().split('\r\n')
    return arduinoData[0]

def printToFile(data, index):
    dataFile.write(data)
    if index != (numPoints - 1):
        dataFile.write(',')
    else:
        dataFile.write('\n')

def getAverage(dataSet, row):
    dataAvg = sum(dataSet) / len(dataSet)
    print('Average for ' + str(row) + ' is: ' + str(dataAvg))

while True:
    userInput = input('Get data points?')

    if userInput == 'y':
        for row in range(numRowsCollect):
            for i in range(numPoints):
                data = getValues()
                printToFile(data, i)
                # print(data)
                dataInt = int(data)
                dataList[i] = dataInt
            
            getAverage(dataList, row)

        dataFile.close()
        break