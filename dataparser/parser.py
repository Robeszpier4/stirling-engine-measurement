import serial as ser
import serial.tools.list_ports
import sys

# 1, connection -> success, 0, 0 -> could not connect to pico
def connectToPico():
    userBaud = int(input("What should be the baudrate of the connection? "))

    comports = serial.tools.list_ports.comports()

    for comport in comports:
        if comport.vid == 0x2E8A:
            try:
                connection = serial.Serial(comport.device, userBaud, timeout=1)

                return connection
            except:
                print("Couldn't connect to pico!")
                sys.exit()

picoConnection = connectToPico()

userFilename = input("What should be the name of the file? ")

with open(userFilename, "w") as logFile: