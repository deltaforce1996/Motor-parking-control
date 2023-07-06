import odrive
from odrive.enums import *
import time
from tqdm import tqdm

WAITING_TIME_LOOP = 0.2

# ============================ Odrive ===============================
def read_all_errors():
    print("************************ Read Error *******************************")
    print("*    ODrive errors: ", ODriveError(odrv0.error).name)
    print("*    Axis0 errors: ", AxisError(odrv0.axis0.error).name)
    print("*    Axis0 motor errors: ", MotorError(odrv0.axis0.motor.error).name)
    print("*    Axis0 controller errors: ", ControllerError(odrv0.axis0.controller.error).name)
    print("********************************************************************")

def set_init_config():
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

    odrv0.axis0.controller.config.vel_limit = 50
    odrv0.axis0.controller.config.pos_gain = 30
    odrv0.axis0.controller.config.vel_gain = 0.02
    odrv0.axis0.controller.config.vel_integrator_gain = 0.2
    odrv0.axis0.trap_traj.config.vel_limit = 30
    odrv0.axis0.trap_traj.config.accel_limit = 5
    odrv0.axis0.trap_traj.config.decel_limit = 5

def set_odrive_config_position_control():
    print("Setup Odrive CTRL_POSITION_CONTROL Parameter...")
    odrv0.axis0.controller.config.control_mode = ControlMode.POSITION_CONTROL   
    odrv0.axis0.controller.config.input_mode = InputMode.TRAP_TRAJ
    # while True:
    #     odrv0.axis0.controller.config.control_mode = ControlMode.POSITION_CONTROL   
    #     odrv0.axis0.controller.config.input_mode = InputMode.TRAP_TRAJ
    #     print("Control Mode:", ControlMode(odrv0.axis0.controller.config.control_mode).name)
    #     print("Input Mode:", InputMode(odrv0.axis0.controller.config.input_mode).name)
    #     if (odrv0.axis0.controller.config.control_mode == ControlMode.POSITION_CONTROL.value or odrv0.axis0.controller.config.input_mode == InputMode.TRAP_TRAJ.value):
    #         break
    #     time.sleep(WAITING_TIME_LOOP)

def set_odrive_config_velocity_control():
    print("Setup Odrive CTRL_VELOCITY_CONTROL Parameter...")
    odrv0.axis0.controller.config.control_mode = ControlMode.VELOCITY_CONTROL
    odrv0.axis0.controller.config.input_mode = InputMode.PASSTHROUGH
    # while True:
    #     odrv0.axis0.controller.config.control_mode = ControlMode.VELOCITY_CONTROL
    #     odrv0.axis0.controller.config.input_mode = InputMode.PASSTHROUGH
    #     print("Control Mode:", ControlMode(odrv0.axis0.controller.config.control_mode).name)
    #     print("Input Mode:", InputMode(odrv0.axis0.controller.config.input_mode).name)
    #     if (odrv0.axis0.controller.config.control_mode == ControlMode.VELOCITY_CONTROL.value or odrv0.axis0.controller.config.input_mode == InputMode.PASSTHROUGH.value):
    #         break
    #     time.sleep(WAITING_TIME_LOOP)

def read_estimate_position():
    return odrv0.axis0.encoder.pos_estimate
# ============================ Motor ===============================
def wait_to_idel():
    while odrv0.axis0.current_state != AxisState.IDLE:
        print(AxisState(odrv0.axis0.current_state).name)
        time.sleep(WAITING_TIME_LOOP)

def motor_idel():
    odrv0.axis0.requested_state = AxisState.IDLE
    # while True:
    #     odrv0.axis0.requested_state = AxisState.IDLE
    #     is_idle = (odrv0.axis0.requested_state == AxisState.IDLE)
    #     print("motor state is idle: ", is_idle)
    #     if (is_idle):
    #         break
    #     time.sleep(WAITING_TIME_LOOP)

def motor_closed_loop_control():
    odrv0.axis0.requested_state = AxisState.CLOSED_LOOP_CONTROL
    # while True:
    #     odrv0.axis0.requested_state = AxisState.CLOSED_LOOP_CONTROL
    #     is_close_loop_conrol = (odrv0.axis0.requested_state == AxisState.CLOSED_LOOP_CONTROL.value)
    #     print("motor id closed loop control: ", is_close_loop_conrol)
    #     if(is_close_loop_conrol):
    #         break
    #     time.sleep(WAITING_TIME_LOOP)

def calibration_sequence():
    print(AxisState(odrv0.axis0.current_state).name)
    odrv0.axis0.requested_state = AxisState.MOTOR_CALIBRATION
    wait_to_idel()

    print(AxisState(odrv0.axis0.current_state).name)
    odrv0.axis0.requested_state = AxisState.ENCODER_INDEX_SEARCH
    wait_to_idel()

    print(AxisState(odrv0.axis0.current_state).name)
    odrv0.axis0.requested_state = AxisState.ENCODER_OFFSET_CALIBRATION
    wait_to_idel()
# ======================================= Main =================================
print("Finding an ODrive...")
odrv0 = odrive.find_any()

odrv0.clear_errors()
motor_idel()
set_init_config()
calibration_sequence()
read_all_errors()
odrv0.clear_errors()

while True:
    set_odrive_config_position_control()
    wait_to_idel()
    motor_closed_loop_control()

    print("Set Zeoro Position...")
    odrv0.axis0.controller.input_pos = 0

    while True:
        if(read_estimate_position() <= 0):
            break
        time.sleep(WAITING_TIME_LOOP)

    target_position = 100
    progress_bar = tqdm(total=target_position, desc='Movement', unit='pos')
    odrv0.axis0.controller.input_pos = target_position

    while True:
        pos_estimate = read_estimate_position()
        progress_fraction = min(pos_estimate / target_position, 1.0)
        progress_bar.n = round(progress_fraction * progress_bar.total)
        progress_bar.refresh()
        if (pos_estimate >= target_position):
            progress_bar.close()
            motor_idel()
            break

    wait_to_idel()
    set_odrive_config_velocity_control()

    while odrv0.axis0.encoder.vel_estimate > 3:
        time.sleep(WAITING_TIME_LOOP)

    wait_to_idel()
    motor_closed_loop_control()

    print("Set Velocity....")
    odrv0.axis0.controller.input_vel = -1
    previous_position = 0
    my_list = []

    while True:
        current_position = read_estimate_position()
        position_change = abs(current_position - previous_position)
        print("Position Change: ", position_change, "  Vel: ", odrv0.axis0.encoder.vel_estimate)

        if (position_change < 0.2):
            my_list.append(True)
        else:
            my_list.clear()

        if (len(my_list) > 7 or current_position < 0.2):
                break
        previous_position = current_position
        time.sleep(WAITING_TIME_LOOP)

    motor_idel()
    read_all_errors()
    odrv0.clear_errors()

    time.sleep(5)


