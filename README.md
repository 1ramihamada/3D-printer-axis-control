# 3D Printer Axis Control via Keyboard

This Python script allows you to manually control the X, Y, and Z axes of a 3D printer using your keyboard. It leverages a serial connection to send G-code commands directly to the printer. The script uses the `pynput` library to capture keyboard input and supports continuous movement while keys are held.

## Features

- **Manual Control**: Use keyboard keys to jog the printer axes interactively.
- **Axis Movements**:
  - `Arrow Keys`: Move X and Y axes.
  - `W/S`: Move the Z-axis up and down.
- **Home Command**: Press `H` to home all axes.
- **Quit Command**: Press `Q` to exit the script.
- **Adjustable Settings**: Configure move increments, feed rates, and serial connection parameters.

## Requirements

- Python 3.x
- A 3D printer with G-code support and serial communication (tested with Prusa i3 MK3S+).
- Required Python libraries:
  - `pynput`
  - `pyserial`

## Installation

1. Clone this repository or download the script:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   pip install pynput pyserial
   ```
## Configuration

- **Serial Connection:**
  - `SERIAL_PORT = '/dev/ttyACM0'`: Update to match your printer's port.
  - `BAUD_RATE = 115200`: Printer's baud rate.
- **Movement Settings:**
  - `MOVE_INCREMENT = 1.0`: Increment for X/Y movements in mm.
  - `Z_INCREMENT = 0.5`: Increment for Z movements in mm.
  - `FEEDRATE_X = 3000`: Feedrate for X-axis in mm/min.
  - `FEEDRATE_Y = 3000`: Feedrate for Y-axis in mm/min.
  - `FEEDRATE_Z = 600`: Feedrate for Z-axis in mm/min
- **Timing:**
  - `time.sleep(0.05)`: Delay for X/Y commands.
  - `time.sleep(0.1)`: Delay for Z commands.


   
