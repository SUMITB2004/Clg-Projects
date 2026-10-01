import socket
import pyautogui
import time

pyautogui.FAILSAFE = False

HOST = '10.223.21.50'
PORT = 8888

OFFSET_X = 4
OFFSET_Y = 0
SPEED = 2

print("Connecting to GestureGlove...")

while True:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        print("Connected! Move your hand to control mouse.")

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
                    if len(values) == 4:
                        tiltX = int(float(values[0])) - OFFSET_X
                        tiltY = int(float(values[1])) - OFFSET_Y
                        flex1 = int(float(values[2]))
                        flex2 = int(float(values[3]))

                        # Fixed mapping:
                        # tilt left/right → mouse left/right = tiltX
                        # tilt up/down → mouse up/down = tiltY
                        mouseX = -tiltY * SPEED  # invert Y for left/right
                        mouseY = -tiltX * SPEED  # invert X for up/down

                        pyautogui.moveRel(mouseX, mouseY, duration=0)

                        if flex1 > 500:
                            pyautogui.click(button='left')
                        if flex2 > 500:
                            pyautogui.click(button='right')

    except KeyboardInterrupt:
        print("Stopped!")
        s.close()
        break
    except Exception as e:
        print(f"Error: {e}, retrying...")
        time.sleep(2)