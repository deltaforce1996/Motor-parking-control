import odrive
from odrive.enums import *
import time
from tqdm import tqdm


def read_all_errors():
    print("************************ Read Error *******************************")
    print("*    ODrive errors: ", ODriveError(odrv0.error).name)
    print("*    Axis0 errors: ", AxisError(odrv0.axis0.error).name)
    print("*    Axis0 motor errors: ", MotorError(odrv0.axis0.motor.error).name)
    print("*    Axis0 controller errors: ", ControllerError(odrv0.axis0.controller.error).name)
    print("********************************************************************")

def read_wait_to_idel():
    while odrv0.axis0.current_state != AxisState.IDLE:
        print(AxisState(odrv0.axis0.current_state).name)
        time.sleep(0.2)

def set_odrive_config_position_control():
    print("Setup Odrive CTRL_POSITION_CONTROL Parameter...")
    odrv0.config.brake_resistance = 2.0
    odrv0.config.dc_bus_undervoltage_trip_level = 8.0
    odrv0.config.dc_bus_overvoltage_trip_level = 56.0
    odrv0.config.dc_max_positive_current = 20.0
    odrv0.config.dc_max_negative_current = -3.0
    odrv0.config.max_regen_current = 0

    odrv0.axis0.motor.config.pole_pairs = 7
    odrv0.axis0.motor.config.calibration_current = 5
    odrv0.axis0.motor.config.resistance_calib_max_voltage = 2
    odrv0.axis0.motor.config.motor_type = MotorType.HIGH_CURRENT
    odrv0.axis0.motor.config.current_lim = 15
    odrv0.axis0.motor.config.requested_current_range = 20

    odrv0.axis0.encoder.config.cpr = 2048
    odrv0.axis0.encoder.config.bandwidth = 3000
    odrv0.axis0.config.calibration_lockin.current = 5
    odrv0.axis0.config.calibration_lockin.ramp_time = 0.4
    odrv0.axis0.config.calibration_lockin.ramp_distance = 3.145927410125732
    odrv0.axis0.config.calibration_lockin.accel = 20
    odrv0.axis0.config.calibration_lockin.vel = 40

    odrv0.axis0.controller.config.control_mode = ControlMode.POSITION_CONTROL
    odrv0.axis0.controller.config.vel_limit = 50
    odrv0.axis0.controller.config.pos_gain = 30
    odrv0.axis0.controller.config.vel_gain = 0.02
    odrv0.axis0.controller.config.vel_integrator_gain = 0.2
    odrv0.axis0.controller.config.input_mode = InputMode.TRAP_TRAJ
    odrv0.axis0.trap_traj.config.vel_limit = 30
    odrv0.axis0.trap_traj.config.accel_limit = 5
    odrv0.axis0.trap_traj.config.decel_limit = 5

def set_odrive_config_velocity_control():
    print("Setup Odrive CTRL_VELOCITY_CONTROL Parameter...")
    odrv0.axis0.controller.config.control_mode = ControlMode.VELOCITY_CONTROL
    odrv0.axis0.controller.config.input_mode = InputMode.PASSTHROUGH

def motor_idel():
    odrv0.axis0.requested_state = AxisState.IDLE
    print("motor idle")

def motor_closed_loop_control():
    odrv0.axis0.requested_state = AxisState.CLOSED_LOOP_CONTROL
    print("motor closed loop control")

def calibration_sequence():
    print(AxisState(odrv0.axis0.current_state).name)
    odrv0.axis0.requested_state = AxisState.MOTOR_CALIBRATION
    read_wait_to_idel()

    print(AxisState(odrv0.axis0.current_state).name)
    odrv0.axis0.requested_state = AxisState.ENCODER_INDEX_SEARCH
    read_wait_to_idel()

    print(AxisState(odrv0.axis0.current_state).name)
    odrv0.axis0.requested_state = AxisState.ENCODER_OFFSET_CALIBRATION
    read_wait_to_idel()


# Find an ODrive
print("Finding an ODrive...")
odrv0 = odrive.find_any()
odrv0.clear_errors()
motor_idel()

set_odrive_config_position_control()
calibration_sequence()
read_all_errors()
odrv0.clear_errors()

print("Control Mode:", ControlMode(odrv0.axis0.controller.config.control_mode).name)
read_wait_to_idel()

motor_closed_loop_control()
time.sleep(0.5)

target_position = 30
progress_bar = tqdm(total=target_position, desc='Movement', unit='pos')
odrv0.axis0.controller.input_pos = target_position

isContinune = True
while isContinune:
    pos_estimate = odrv0.axis0.encoder.pos_estimate
    pos_estimate < target_position
    progress_fraction = min(pos_estimate / target_position, 1.0)
    progress_bar.n = round(progress_fraction * progress_bar.total)
    progress_bar.refresh()
    if pos_estimate > target_position/2:
        progress_bar.close()
        isContinune = False
        motor_idel()

read_wait_to_idel()

set_odrive_config_velocity_control()

print("Control Mode:", ControlMode(odrv0.axis0.controller.config.control_mode).name)
time.sleep(0.5)

while odrv0.axis0.encoder.vel_estimate > 3:
    time.sleep(0.2)

read_wait_to_idel()
motor_closed_loop_control()

odrv0.axis0.controller.input_vel = -8

previous_position = odrv0.axis0.encoder.pos_estimate
my_list = []
while True:
    current_position = odrv0.axis0.encoder.pos_estimate
    position_change = abs(current_position - previous_position)
    print("Position Change: ", position_change, "  Vel: ", odrv0.axis0.encoder.vel_estimate)
    if position_change < 0.5:
        my_list.append(True)
        if len(my_list) > 7:
            break
    else:
        my_list.clear()

    previous_position = current_position
    time.sleep(0.2)

motor_idel()
read_all_errors()
odrv0.clear_errors()


