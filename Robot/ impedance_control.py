import odrive
from odrive.enums import *
from odrive.enums import ControlMode
from odrive.utils import dump_errors  
import time

# Connect to the ODrive
odrv0 = odrive.find_any()

odrv0.axis0.controller.config.control_mode = ControlMode.POSITION_CONTROL

dump_errors(odrv0)
odrv0.clear_errors()

odrv0.axis0.controller.config.control_mode = ControlMode.TORQUE_CONTROL

# Approximately 8.27 / Kv where Kv is in the units [rpm / V]
# odrv0.axis0.config.motor.torque_constant = 8.27 / 31

odrv0.axis0.controller.input_torque = 0.1