import serial
import time

print("Scanning for GestureGlove...")
while True:
    for p in ['COM3','COM4','COM5','COM6','COM8','COM9','COM11','COM12','COM13']:
        try:
            ser = serial.Serial(p, 9600, timeout=1)
            print(f"✅ Found on {p}!")
            while True:
                if ser.in_waiting:
                    print(ser.readline().decode(errors='ignore').strip())
        except:
            pass
    time.sleep(1)