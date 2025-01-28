import time
import serial

ser = serial.Serial("/dev/ttyUSB0", baudrate=1200)

ser.write(b"~20014682C0048520FCC3\r")

time.sleep(1)

ser.close()

time.sleep(0.1)

ser = serial.Serial("/dev/ttyUSB0", baudrate=115200)

# ser.write(b'pwr\n')
ser.write(b"bat\n")

resp = ""
while ser.in_waiting != 0:
    resp += ser.read().decode()
print(resp)

ser.close()
