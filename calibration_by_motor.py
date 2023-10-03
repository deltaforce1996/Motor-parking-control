from controllers_sim.odrive_controller import ODriveController
from controllers_sim.motor_controller import MotorController
from helpers.axis_params import AxisParameter
import odrive
import time


print("Finding an ODrive...")
odrv0 = odrive.find_any()
odrive_controller = ODriveController(odrv0)
motor_controller = MotorController(odrive_controller, "axis0")

odrive_controller.clear_errors()
motor_controller.motor_calibrate_control()
motor_controller.wait_to_idel()
time.sleep(2)
motor_controller.motor_index_search()
motor_controller.wait_to_idel()
time.sleep(2)
motor_controller.motor_index_encoder_offset()
motor_controller.wait_to_idel()
time.sleep(2)
motor_controller.set_axis_parameter(AxisParameter.ENCODER_CONF_PRE_CALI, 1, True)

motor_controller.read_errors()

#motor calibration
#index search 
#index offset
#motor pre calibration = 1