import odrive
from tqdm import tqdm
from controllers.odrive_controller import ODriveController
from controllers.motor_controller import MotorController
import time

WAITING_TIME_LOOP = 0.2
my_list = []

print("Finding an ODrive...")
odrv0 = odrive.find_any()
odrive_controller = ODriveController(odrv0)
motor_controller = MotorController(odrive_controller, "axis0")

odrive_controller.clear_errors()
odrive_controller.set_init_configs()
motor_controller.set_init_configs()
motor_controller.calibration_sequence()
odrive_controller.read_errors()
motor_controller.read_errors()


while True:
    motor_controller.wait_to_idel()
    motor_controller.set_controller_config_position_control()
    motor_controller.motor_closed_loop_control()

    print("Set Zeoro Position...")
    motor_controller.set_position(0)

    while True:
        if motor_controller.read_estimate_position() <= 0:
            break
        time.sleep(WAITING_TIME_LOOP)

    target_position = 100
    progress_bar = tqdm(total=target_position, desc="Movement", unit="pos")
    motor_controller.set_position(target_position)

    while True:
        pos_estimate = motor_controller.read_estimate_position()
        progress_fraction = min(pos_estimate / target_position, 1.0)
        progress_bar.n = round(progress_fraction * progress_bar.total)
        progress_bar.refresh()
        if pos_estimate >= target_position:
            progress_bar.close()
            motor_controller.motor_idel()
            break

    motor_controller.wait_to_idel()
    motor_controller.set_controlller_config_velocity_control()

    while motor_controller.read_estimate_velocity() > 3:
        time.sleep(WAITING_TIME_LOOP)

    motor_controller.motor_closed_loop_control()

    print("Set Velocity...")
    motor_controller.set_velocity(-1)
    previous_position = 0

    while True:
        current_position = motor_controller.read_estimate_position()
        position_change = abs(current_position - previous_position)
        print(
            "Position Change: ",
            position_change,
            "  Vel: ",
            motor_controller.read_estimate_velocity(),
        )

        if position_change < 0.2:
            my_list.append(True)
        else:
            my_list.clear()

        if len(my_list) > 7 or current_position < 0.2:
            break
        previous_position = current_position
        time.sleep(WAITING_TIME_LOOP)

    motor_controller.motor_idel()
    odrive_controller.read_errors()
    motor_controller.read_errors()
    odrive_controller.clear_errors()

    time.sleep(5)
