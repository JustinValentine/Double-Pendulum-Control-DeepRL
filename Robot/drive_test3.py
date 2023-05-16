import odrive
from odrive.enums import *
import time

# Connect to the ODrive
odrv0 = odrive.find_any()

# Calibrate the motors and encoders if required
# Uncomment the following lines if you need to calibrate

odrv0.axis0.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
odrv0.axis1.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
time.sleep(10)  # Wait for calibration to finish

# Set motors to closed loop control
odrv0.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
odrv0.axis1.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL

# Function to move both motors to the desired position
def move_motors(position0, position1):
    odrv0.axis0.controller.input_pos = position0
    odrv0.axis1.controller.input_pos = position1

while True:
    # Get user input for desired positions
    position0 = float(input("Enter the desired position for motor 0: "))
    position1 = float(input("Enter the desired position for motor 1: "))

    # Move the motors to the desired positions
    move_motors(position0, position1)
