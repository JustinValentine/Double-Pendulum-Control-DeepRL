import time
import odrive
from odrive.enums import *

# Connect to the ODrive
print("Connecting to ODrive...")
my_drive = odrive.find_any()
print("Connected to ODrive!")

# Define your motor indices (0 for M0 and 1 for M1)
motor_0 = 0
motor_1 = 1

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

# # Set motor velocities
# velocity_0 = 2  # ticks/s
# velocity_1 = 2  # ticks/s
# my_drive.axis0.controller.vel_setpoint = velocity_0
# my_drive.axis1.controller.vel_setpoint = velocity_1


# # Run motors for 5 seconds
# time.sleep(5)

# # Stop motors
# my_drive.axis0.controller.vel_setpoint = 0
# my_drive.axis1.controller.vel_setpoint = 0
