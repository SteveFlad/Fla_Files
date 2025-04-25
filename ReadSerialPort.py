#ReadSerialPort.py
#This code reads the serial port and prints the data on the console 
import serial

ser = serial.Serial(
    port='COM3',\
    baudrate=9600,\
   )

print("connected to: " + ser.portstr)
count=1

print("Outside while loop")
while True:
    print("Inside while loop")             
    cc=str(ser.readline())
    print(cc)    
    count = count+1
    if count > 20:
            ser.close()
            print("20 records read - connection closed")
            
