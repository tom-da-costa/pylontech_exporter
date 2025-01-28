import time
import serial
import sys, getopt


cmd = " ".join(sys.argv[1:])
print(cmd)

ser = serial.Serial("/dev/ttyUSB0", baudrate=1200)

ser.write(b"~20014682C0048520FCC3\r")

time.sleep(1)

ser.close()

time.sleep(0.1)

ser = serial.Serial("/dev/ttyUSB0", baudrate=115200)

# ser.write(b'pwr\n')
ser.write(bytes(cmd + "\n", "ascii"))


def readAndPrint():
    resp = ""
    while ser.in_waiting != 0:
        resp += ser.read().decode()
    print(resp)


readAndPrint()

# if cmd == "help":wakeup.py
#   for _ in range(5):
#     ser.write(b'\n')
#     time.sleep(0.5)
#     readAndPrint()

ser.close()
