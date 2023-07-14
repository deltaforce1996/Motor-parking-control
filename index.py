import odrive
from tqdm import tqdm
from controllers.odrive_controller import ODriveController
from controllers.motor_controller import MotorController
from helpers.enums import *
import time
import sys
from helpers.axis_params import AxisParameter
import random
import tkinter as tk

WAITING_TIME_LOOP = 0.2
PROXIMITY_SENSOR_PIN = 6

global_current_profile = None

def __fast_profile():
    global global_current_profile
    global_current_profile = "FAST"
    motor_controller.set_axis_parameter(AxisParameter.TRAP_TRAJ_VEL_LIMIT, 30)
    motor_controller.set_axis_parameter(AxisParameter.TRAP_TRAJ_DECEL_LIMIT, 15)
    motor_controller.set_axis_parameter(AxisParameter.TRAP_TRAJ_ACCEL_LIMIT, 15)

def __slow_profile():
    global global_current_profile
    global_current_profile = "SLOW"
    motor_controller.set_axis_parameter(AxisParameter.TRAP_TRAJ_VEL_LIMIT, 30)
    motor_controller.set_axis_parameter(AxisParameter.TRAP_TRAJ_DECEL_LIMIT, 0.5)
    motor_controller.set_axis_parameter(AxisParameter.TRAP_TRAJ_ACCEL_LIMIT, 2)

def setup_and_calibration():
    odrive_controller.clear_errors()
    odrive_controller.set_init_configs()
    motor_controller.set_init_configs()
    __slow_profile()
    odrive_controller.set_config_gpio_mode(PROXIMITY_SENSOR_PIN, GpioMode.DIGITAL.value)
    motor_controller.set_min_endstop(PROXIMITY_SENSOR_PIN)
    odrive_controller.set_config_gpio_mode(PROXIMITY_SENSOR_PIN, GpioMode.DIGITAL_PULL_UP.value)
    motor_controller.calibration_sequence()
    odrive_controller.read_errors()
    motor_controller.read_errors()

def set_position_mode():
    motor_controller.motor_idel()
    motor_controller.wait_to_idel()
    motor_controller.set_controller_config_position_control()
    motor_controller.set_enable_min_endstop(True)
    
def set_position_to_zero():
    set_position_mode()
    motor_controller.motor_closed_loop_control()
    print("Set Zeoro Position...")
    motor_controller.set_position(0)
    while True:
        if motor_controller.read_motor_minstop_state():
            break
        pos_estimate = motor_controller.read_estimate_position()
        if(pos_estimate < 0.001):
            break
    __slow_profile()

def start_parking_torque_control():
    my_list = []
    motor_controller.motor_idel()
    motor_controller.wait_to_idel()
    motor_controller.set_controller_config_control_torque_mode()
    motor_controller.set_enable_min_endstop(True)
    torque_input = float(input("Enter torque target: "))
    motor_controller.motor_closed_loop_control()
    motor_controller.set_torque(torque_input)
    print("Set torque....")
    previous_position = 0
    no_change_counter = 0

    while True:
        current_position = motor_controller.read_estimate_position()
        position_change = abs(current_position - previous_position)
        
        no_change_counter += 1
        sys.stdout.write('\r' + "Parking" + '.' * no_change_counter)
        sys.stdout.flush()
        
        if position_change < 0.1:
            my_list.append(True)
        else:
            my_list.clear()

        if len(my_list) > 10:
            break
        previous_position = current_position
        time.sleep(WAITING_TIME_LOOP)
    print("")
    motor_controller.set_velocity(0)
    motor_controller.motor_idel()
    odrive_controller.read_errors()
    motor_controller.read_errors()
    odrive_controller.clear_errors()
    __slow_profile()

def move_to_target_position():
    set_position_mode()
    motor_controller.motor_closed_loop_control()
    target_position = float(input("Set Target Position: "))
    print("Set Target Position...")
    motor_controller.set_position(target_position)
    progress_bar = tqdm(total=target_position, desc="Movement", unit="pos")

    while True:
        if motor_controller.read_motor_minstop_state():
            progress_bar.close()
            motor_controller.motor_idel()
            break

        current_position = motor_controller.read_estimate_position()

        progress_fraction = min(current_position / target_position, 1.0)
        progress_bar.n = round(progress_fraction * progress_bar.total)
        progress_bar.refresh()
        if (round(current_position, 3) == round(target_position, 3)):
            progress_bar.close()
            motor_controller.motor_idel()
            __slow_profile()
            break

def start_homing():
    set_position_mode()
    motor_controller.motor_closed_loop_control()
    motor_controller.motor_homing()
    motor_controller.wait_to_idel()

def start_parking_velocity_control():
    my_list = []
    motor_controller.motor_idel()
    motor_controller.wait_to_idel()
    motor_controller.set_enable_min_endstop(False)
    motor_controller.set_controlller_config_velocity_control()
    motor_controller.motor_closed_loop_control()
    decel_input = float(input("Enter deceleration value: "))
    accel_input = float(input("Enter acceleration value: "))
    velocity_limit_input = float(input("Enter velocity limit: "))
    motor_controller.set_axis_parameter(AxisParameter.CONTROL_CONF_VEL_LIMIT, velocity_limit_input)
    motor_controller.set_axis_parameter(AxisParameter.TRAP_TRAJ_DECEL_LIMIT, decel_input)
    motor_controller.set_axis_parameter(AxisParameter.TRAP_TRAJ_ACCEL_LIMIT, accel_input)
    velocity_input = float(input("Enter velocity target: "))
    motor_controller.set_velocity(velocity_input)
    print("Set Velocity...")
    previous_position = 0
    no_change_counter = 0

    while True:
        current_position = motor_controller.read_estimate_position()
        position_change = abs(current_position - previous_position)
        
        no_change_counter += 1
        sys.stdout.write('\r' + "Parking" + '.' * no_change_counter)
        sys.stdout.flush()
        
        if position_change < 0.2:
            my_list.append(True)
        else:
            my_list.clear()

        if len(my_list) > 10:
            break
        previous_position = current_position
        time.sleep(WAITING_TIME_LOOP)
    print("")
    motor_controller.set_velocity(0)
    motor_controller.motor_idel()
    odrive_controller.read_errors()
    motor_controller.read_errors()
    odrive_controller.clear_errors()
    __slow_profile()

def start_parking_position_control():
    my_list = []
    motor_controller.motor_idel()
    motor_controller.wait_to_idel()
    motor_controller.set_enable_min_endstop(False)
    motor_controller.set_controller_config_position_control()
    decel_input = float(input("Enter deceleration value: "))
    accel_input = float(input("Enter acceleration value: "))
    target_input = float(input("Enter position target: "))
    motor_controller.set_axis_parameter(AxisParameter.TRAP_TRAJ_DECEL_LIMIT, decel_input)
    motor_controller.set_axis_parameter(AxisParameter.TRAP_TRAJ_ACCEL_LIMIT, accel_input)
    motor_controller.motor_closed_loop_control()
    motor_controller.set_position(target_input)
    print("Set Position...")
    previous_position = 0
    no_change_counter = 0

    while True:
        current_position = motor_controller.read_estimate_position()
        position_change = abs(current_position - previous_position)
        
        no_change_counter += 1
        sys.stdout.write('\r' + "Parking" + '.' * no_change_counter)
        sys.stdout.flush()
        
        if position_change < 0.2:
            my_list.append(True)
        else:
            my_list.clear()

        if len(my_list) > 10:
            break
        previous_position = current_position
        time.sleep(WAITING_TIME_LOOP)
    print("")
    motor_controller.set_velocity(0)
    motor_controller.motor_idel()
    odrive_controller.read_errors()
    motor_controller.read_errors()
    odrive_controller.clear_errors()
    __slow_profile()

def clear_errors():
    odrive_controller.clear_errors()

def read_error():
    odrive_controller.read_errors()
    motor_controller.read_errors()

def reset_odrive_config():
    odrive_controller.reset_config()

print("Finding an ODrive...")
odrv0 = odrive.find_any()
odrive_controller = ODriveController(odrv0)
motor_controller = MotorController(odrive_controller, "axis0")

def on_slide(value):
    motor_controller.set_position(value)

def moving_control():
    set_position_mode()
    decel_input = float(input("Enter deceleration value: "))
    accel_input = float(input("Enter acceleration value: "))
    motor_controller.set_axis_parameter(AxisParameter.TRAP_TRAJ_DECEL_LIMIT, decel_input)
    motor_controller.set_axis_parameter(AxisParameter.TRAP_TRAJ_ACCEL_LIMIT, accel_input)
    motor_controller.motor_closed_loop_control()
    root = tk.Tk()
    slider = tk.Scale(root, from_=-100, to=100, orient=tk.HORIZONTAL, command=on_slide)
    slider.pack()
    root.mainloop()
    __slow_profile()

while True:
    print("******* Profile ", global_current_profile)
    print("****************************** Please select Commands Id *********************************")
    print("*              1. Need cralibration             12. Moving axis                          *")
    print("*              2. Move to zero                  13. Parking position                     *")
    print("*              3. Move to 100                                                            *")
    print("*              4. Parking velocity                                                       *") 
    print("*              5. Clear errors                                                           *")
    print("*              6. Start homing                                                           *")
    print("*              7. Read error                                                             *")
    print("*              8. Parking torque                                                         *")
    print("*              9. Reset configs                                                          *")
    print("*              10. Select slow profile                                                   *")
    print("*              11. Select fast profile                                                   *")
    print("*****************************************************************************************")

    cmd_id_input = input("Enter Your Command Id: ")
    cmd_id = int(cmd_id_input)

    if cmd_id == 1:
        setup_and_calibration()
    elif cmd_id == 2:
        set_position_to_zero()
    elif cmd_id == 3:
        move_to_target_position()
    elif cmd_id == 4:
        start_parking_velocity_control()
    elif cmd_id == 5:
        clear_errors()
    elif cmd_id == 6:
        start_homing()
    elif cmd_id == 7:
        read_error()
    elif cmd_id == 8:
        start_parking_torque_control()
    elif cmd_id == 9:
        reset_odrive_config()
    elif cmd_id == 10:
        __slow_profile()
    elif cmd_id == 11:
        __fast_profile()
    elif cmd_id == 12:
        moving_control()
    elif cmd_id == 13:
        start_parking_position_control()
    else:
        print("Unknow CMD!!!")

