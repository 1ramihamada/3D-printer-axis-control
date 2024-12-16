import serial
import time
from pynput import keyboard

# --- User Configuration ---
SERIAL_PORT = '/dev/ttyACM0'  # Adjust if needed
BAUD_RATE = 115200
MOVE_INCREMENT = 1.0  # mm per increment step
Z_INCREMENT = 0.5
FEEDRATE_X = 3000        # Higher feedrate for quicker response
FEEDRATE_Y = 3000 
FEEDRATE_Z = 600 

# Connect to the printer
ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=2)
time.sleep(2)  # Wait for the printer to initialize
ser.write(b"G91\n")  # Relative positioning
ser.flush()

print(f"Connected to printer on {SERIAL_PORT} at {BAUD_RATE} baud.")
print("Hold arrow keys to move X/Y continuously, W/S for Z, Q to quit, H to home.")

# Track which keys are currently pressed
pressed_keys = {
    'up': False,
    'down': False,
    'left': False,
    'right': False,
    'w': False,
    's': False,
}

running = True

def send_gcode(cmd):
    ser.write((cmd + "\n").encode('utf-8'))
    ser.flush()

def on_press(key):
    global running
    try:
        if key == keyboard.Key.up:
            pressed_keys['up'] = True
        elif key == keyboard.Key.down:
            pressed_keys['down'] = True
        elif key == keyboard.Key.left:
            pressed_keys['left'] = True
        elif key == keyboard.Key.right:
            pressed_keys['right'] = True
        else:
            if key.char == 'w':
                pressed_keys['w'] = True
            elif key.char == 's':
                pressed_keys['s'] = True
            elif key.char == 'q':
                # Stop running
                running = False
                return False
            elif key.char == 'h':
                # Home the device
                send_gcode("G90")   # Switch to absolute positioning
                send_gcode("G28")   # Home all axes
                send_gcode("G91")   # Return to relative positioning after homing
                print("Homing...")

    except AttributeError:
        # For keys without a char attribute (like arrows), we already handled them above
        pass

def on_release(key):
    try:
        if key == keyboard.Key.up:
            pressed_keys['up'] = False
        elif key == keyboard.Key.down:
            pressed_keys['down'] = False
        elif key == keyboard.Key.left:
            pressed_keys['left'] = False
        elif key == keyboard.Key.right:
            pressed_keys['right'] = False
        else:
            if hasattr(key, 'char'):
                if key.char == 'w':
                    pressed_keys['w'] = False
                elif key.char == 's':
                    pressed_keys['s'] = False
    except AttributeError:
        pass

# Start the listener
listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()

try:
    while running:
        # Move Y axis (Up / Down)
        if pressed_keys['up']:
            send_gcode(f"G1 Y{MOVE_INCREMENT} F{FEEDRATE_Y}")
        if pressed_keys['down']:
            send_gcode(f"G1 Y-{MOVE_INCREMENT} F{FEEDRATE_Y}")

        # Move X axis (Left / Right)
        if pressed_keys['left']:
            send_gcode(f"G1 X-{MOVE_INCREMENT} F{FEEDRATE_X}")
        if pressed_keys['right']:
            send_gcode(f"G1 X{MOVE_INCREMENT} F{FEEDRATE_X}")

        # Move Z axis (W / S)
        if pressed_keys['w']:
            send_gcode(f"G1 Z{Z_INCREMENT} F{FEEDRATE_Z}")
        if pressed_keys['s']:
            send_gcode(f"G1 Z-{Z_INCREMENT} F{FEEDRATE_Z}")

        # Adjust this delay as necessary
        time.sleep(0.05)

finally:
    # Return to absolute positioning before exit
    ser.write(b"G90\n")  
    ser.flush()
    ser.close()
    print("Disconnected and returned to absolute positioning.")