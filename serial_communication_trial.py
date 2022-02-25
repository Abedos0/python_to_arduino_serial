
import serial
import time
ser = serial.Serial(baudrate=115200, timeout=0.5, port='COM3')
time.sleep(2)
print(ser)
command = b'start#delay#stop'
print(command)
ser.write(command)
print("Check response")
for _ in range(5):
    print(ser.readline())
    time.sleep(0.2)
ser.close()
