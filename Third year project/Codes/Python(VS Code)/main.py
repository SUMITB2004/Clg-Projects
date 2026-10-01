import socket
import pyautogui
import time

pyautogui.FAILSAFE = False

HOST = '10.223.21.50'   # ESP32 WiFi IP
PORT = 8888

OFFSET_X = 4           # calibrate this later
OFFSET_Y = 0
SPEED = 2              # adjust for comfortable cursor speed

FLEX1_THRESHOLD = 100  # tune after testing straight vs bent

print("Connecting to GestureGlove...")

while True:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        print("Connected!")

        buffer = ""
        while True:
            data = s.recv(4096).decode(errors='ignore')
            if not data:
                break

            buffer += data
            lines = buffer.split('\n')
            buffer = lines[-1]

            if len(lines) > 1:
                line = lines[-2].strip()
                if line:
                    values = line.split(',')
                    if len(values) == 3:
                        tiltX = int(float(values[0])) - OFFSET_X
                        tiltY = int(float(values[1])) - OFFSET_Y
                        flex1 = int(float(values[2]))

                        print(f"tiltX:{tiltX} tiltY:{tiltY} flex1:{flex1}")

                        # FIX all directions HERE:
                        #
                        # Logic: 
                        # - Tilt left/right  → mouse left/right   = +tiltX
                        # - Tilt up/down     → mouse up/down      = -tiltY
                        #
                        mouseX = tiltX * SPEED    # left/right from tiltX
                        mouseY = -tiltY * SPEED   # up/down from tiltY (negative)

                        pyautogui.moveRel(mouseX, mouseY, duration=0)

                        if flex1 > FLEX1_THRESHOLD:
                            pyautogui.click(button='left')


                            print("LEFT CLICK")

    except KeyboardInterrupt:
        print("Stopped!")
        s.close()
        break
    except Exception as e:
        print(f"Error: {e}, retrying...")
        time.sleep(2)