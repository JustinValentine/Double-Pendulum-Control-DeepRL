import odrive
from odrive.enums import *
from odrive.enums import ControlMode
from odrive.utils import dump_errors  
import time

# Connect to the ODrive
odrv0 = odrive.find_any()

dump_errors(odrv0)
odrv0.clear_errors()

# Calibrate the motors and encoders if required
# odrv0.axis0.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
# odrv0.axis1.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
# time.sleep(10)  # Wait for calibration to finish

odrv0.axis0.requested_state = AXIS_STATE_IDLE
odrv0.axis1.requested_state = AXIS_STATE_IDLE
time.sleep(0.5)

# Check that both axes are idle
if odrv0.axis0.current_state != AXIS_STATE_IDLE or odrv0.axis1.current_state != AXIS_STATE_IDLE:
    print("Ensure both motors are in the AXIS_STATE_IDLE state before proceeding.")
    exit()

# Set closed-loop control mode for both axes
odrv0.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
odrv0.axis1.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL

# Set control mode to position control for both axes
odrv0.axis0.controller.config.control_mode = ControlMode.POSITION_CONTROL
odrv0.axis1.controller.config.control_mode = ControlMode.POSITION_CONTROL

AXIS1_OFFSET = 0.38

odrv0.axis0.controller.input_pos = 0
odrv0.axis1.controller.input_pos = 0 + AXIS1_OFFSET
time.sleep(3)

try:
    while True:
        # Read the position of axis0
        axis0_position = odrv0.axis0.encoder.pos_estimate
        axis1_position = odrv0.axis1.encoder.pos_estimate

        print("Axis 0 position: {:.4f}".format(axis0_position))
        print("Axis 1 position: {:.4f}".format(axis1_position - AXIS1_OFFSET))


        # Set the position of axis1 to match axis0 position
        odrv0.axis0.controller.input_pos = axis1_position - AXIS1_OFFSET
        odrv0.axis1.controller.input_pos = axis0_position + AXIS1_OFFSET

        # Wait a short time to avoid overloading the control loop
        time.sleep(0.01)

except KeyboardInterrupt:
    # Stop the motors when you interrupt the script
    odrv0.axis0.requested_state = AXIS_STATE_IDLE
    odrv0.axis1.requested_state = AXIS_STATE_IDLE
