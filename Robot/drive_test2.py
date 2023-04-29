import time
import odrive
from odrive.enums import *

# Connect to the ODrive
print("Connecting to ODrive...")
my_drive = odrive.find_any()
print("Connected to ODrive!")

# Calibrate the motors
print("Calibrating Motor 0...")
my_drive.axis0.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
print("Calibrating Motor 1...")
my_drive.axis1.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE

# Wait for calibration to finish
while my_drive.axis0.current_state != AXIS_STATE_IDLE or my_drive.axis1.current_state != AXIS_STATE_IDLE:
    time.sleep(0.1)

# Set motors to closed-loop control
my_drive.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
my_drive.axis1.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL


my_drive.axis0.controller.input_pos = 1
my_drive.axis1.controller.input_pos = 1

