from controllers_sim.odrive_controller import ODriveController
from controllers_sim.motor_controller import MotorController
from helpers.axis_params import AxisParameter
import odrive
import time
    
def is_traj_pos_done():
   start_time_checking = time.time()
   while True:
      if time.time() - start_time_checking > 50:
         motor_controller.motor_idel()
         print("timeout!")
         return False
      if motor_controller.read_trap_traj_status():
        print("done!")
        return True

print("Finding an ODrive...")
odrv0 = odrive.find_any()
odrive_controller = ODriveController(odrv0)
motor_controller = MotorController(odrive_controller, "axis0")

axis_error = motor_controller.read_axis_err()
motor_controller.set_axis_parameter(AxisParameter.MIN_ENDSTOP_CONF_ENABLE, False)
odrive_controller.clear_errors()
motor_controller.motor_index_search()
motor_controller.set_controller_config_position_control()

# motor_controller.motor_closed_loop_control()
# motor_controller.set_position(-8)
# is_traj_pos_done()
# motor_controller.motor_idel()

if axis_error == 4096:
    motor_controller.motor_closed_loop_control()
    motor_controller.set_position(-3)
    is_traj_pos_done()

motor_controller.motor_idel()
motor_controller.set_axis_parameter(AxisParameter.MIN_ENDSTOP_CONF_ENABLE, True)
motor_controller.set_controlller_config_velocity_control()
motor_controller.motor_closed_loop_control()
motor_controller.set_velocity(-2)

start_time = time.time()
while time.time() - start_time < 50:
    current_Iq = motor_controller.read_estimate_Iq_measured()
    print(abs(current_Iq))
    if abs(current_Iq) > 45:
       motor_controller.motor_idel()
       break

motor_controller.motor_idel()
motor_controller.set_controller_config_position_control()
motor_controller.motor_closed_loop_control()
current_pos = motor_controller.read_estimate_position()
middle_pos = motor_controller.read_estimate_position() + 11
print("current pos : ", current_pos)
print("middle offset : ", middle_pos)
motor_controller.set_position(middle_pos)
is_traj_pos_done()
motor_controller.motor_idel()
print("Homing successfully.")