import odrive
from odrive.enums import *
from odrive.utils import dump_errors  
import time
import matplotlib.pyplot as plt

def plot_data(times, pos0, pos1, vel0, vel1, current0, current1, torque0, torque1):
    # Clear the previous plots
    for a in ax:
        a.clear()

    # Plot the new data for motor 0 (in blue) and motor 1 (in red)
    ax[0].plot(times, pos0, label='Position 0', color='blue')
    ax[0].plot(times, pos1, label='Position 1', color='red')
    ax[1].plot(times, vel0, label='Velocity 0', color='blue')
    ax[1].plot(times, vel1, label='Velocity 1', color='red')
    ax[2].plot(times, current0, label='Current 0', color='blue')
    ax[2].plot(times, current1, label='Current 1', color='red')
    ax[3].plot(times, torque0, label='Torque 0', color='blue')
    ax[3].plot(times, torque1, label='Torque 1', color='red')

    # Set labels and legends
    for i, label in enumerate(['Position', 'Velocity', 'Current', 'Torque']):
        ax[i].set_ylabel(label)
        ax[i].legend()
    ax[3].set_xlabel('Time (s)')

    # Draw the figure on the screen
    fig.canvas.draw()
    fig.canvas.flush_events()

    # Optional: pause a bit for the plot to update
    time.sleep(0.01)

# Lists to store data for both motors
times = []
pos0, pos1 = [], []
vel0, vel1 = [], []
current0, current1 = [], []
torque0, torque1 = [], []

# Create a new figure and axes
plt.ion()
fig, ax = plt.subplots(4, 1, sharex=True)

# Start time
start_time = time.time()

# # == Odrive == # #

# Connect to the ODrive
odrv0 = odrive.find_any()

# Clear any errors 
dump_errors(odrv0)
odrv0.clear_errors()

# Calibrate the motors and encoders if required
odrv0.axis0.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
odrv0.axis1.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
time.sleep(10)

# Set closed-loop control mode for both axes
odrv0.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
odrv0.axis1.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL

# Set control mode to position control for both axes
odrv0.axis0.controller.config.control_mode = ControlMode.POSITION_CONTROL
odrv0.axis1.controller.config.control_mode = ControlMode.POSITION_CONTROL

odrv0.axis0.controller.input_pos = 0
odrv0.axis1.controller.input_pos = 0
move = 0

while True:
    current_time = time.time() - start_time
    pos_0 = odrv0.axis0.encoder.pos_estimate
    vel_0 = odrv0.axis0.encoder.vel_estimate
    current_0 = odrv0.axis0.motor.current_control.Iq_measured
    torque_0 = current_0 * odrv0.axis0.motor.config.torque_constant
