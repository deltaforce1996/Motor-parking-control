from helpers.enums import *
import time
from helpers.device_manager import DeviceManager
from helpers.axis_params import AxisParameter
import sys


class MotorController(DeviceManager):
    def __init__(self, odrive_controller, axis):
        self.__odrv0 = odrive_controller.odrv0
        self.__WAITING_TIME_LOOP = 0.2
        self.__axis = getattr(self.__odrv0, axis)

    def set_axis_parameter(self, param_name, param_value, is_check_param = True):
        attr_names = param_name.split(".")
        attr_aixs =  self.__axis

        for part in attr_names[:-1]:
            attr_aixs = getattr(attr_aixs, part)

        while True:
            setattr(attr_aixs, attr_names[-1], param_value)
            print("Set axis param [", param_name, "] = ", param_value)
            if is_check_param:
                time.sleep(0.020)
                response = getattr(attr_aixs, attr_names[-1])
                if(round(response) == round(param_value)): break
            else:
                break
            time.sleep(self.__WAITING_TIME_LOOP)

    def read_axis_parameter(self, param_name):
        attr_names = param_name.split('.')
        attr_axis = self.__axis
        for part in attr_names:
            attr_axis = getattr(attr_axis, part)
        print("Read axis param [", param_name, "] = ", attr_axis)
        return attr_axis

    def set_init_configs(self):
        self.set_axis_parameter(AxisParameter.MOTOR_CONF_POLE_PAIRS, 7)
        self.set_axis_parameter(AxisParameter.MOTOT_CONF_CALI_CURRENT, 10)
        self.set_axis_parameter(AxisParameter.MOTOT_CONF_RESISTANCE_CALI_MAX_VOLT, 5)
        self.set_axis_parameter(AxisParameter.MOTOR_CONF_MOTOR_TYPE, MotorType.HIGH_CURRENT.value)
        self.set_axis_parameter(AxisParameter.MOTOR_CONF_CURRENT_LIMIT, 20)
        self.set_axis_parameter(AxisParameter.MOTOR_CONF_REQ_CURRENT_RANGE, 10)
        self.set_axis_parameter(AxisParameter.MOTOR_CONF_TORQ_CONST, 8.23 / 150)

        self.set_axis_parameter(AxisParameter.ENCODER_CONF_CPR, 2048)
        self.set_axis_parameter(AxisParameter.ENCODER_CONF_BAND_WIDTH, 3000)

        self.set_axis_parameter(AxisParameter.CONF_CALI_LOCK_CURRENT, 10)
        self.set_axis_parameter(AxisParameter.CONF_CALI_LOCK_RAMP_TIME, 0.4)
        self.set_axis_parameter(AxisParameter.CONF_CALI_LOCK_RAMP_DISTANCE, 3.145927410125732)
        self.set_axis_parameter(AxisParameter.CONF_CALI_LOCK_ACCEL, 20)
        self.set_axis_parameter(AxisParameter.CONF_CALI_LOCK_VEL, 20)

        self.set_axis_parameter(AxisParameter.CONTROL_CONF_VEL_LIMIT, 20)
        self.set_axis_parameter(AxisParameter.CONTROL_CONF_POS_GAIN, 30)
        self.set_axis_parameter(AxisParameter.CONTROL_CONF_VEL_GAIN, 0.4)
        self.set_axis_parameter(AxisParameter.CONTROL_CONF_VEL_INTEGRATOR_GAIN, 0.8)


    def set_min_endstop(self, pin_num):
        self.set_axis_parameter(AxisParameter.MIN_ENDSTOP_CONF_GPIO_NUM, pin_num)
        self.set_axis_parameter(AxisParameter.MIN_ENDSTOP_CONF_IS_ACTIVE_HIGH, False)
        self.set_axis_parameter(AxisParameter.MIN_ENDSTOP_CONF_OFFSET, 0.25)
        self.set_axis_parameter(AxisParameter.MIN_ENDSTOP_CONF_ENABLE, True)
        self.set_axis_parameter(AxisParameter.MIN_ENDSTOP_CONF_DEBONUNCE_MS, 50.0)

    def set_max_endstop(self, pin_num):
        self.set_axis_parameter(AxisParameter.MAX_ENDSTOP_CONF_GPIO_NUM, pin_num)
        self.set_axis_parameter(AxisParameter.MAX_ENDSTOP_CONF_IS_ACTIVE_HIGH, False)
        self.set_axis_parameter(AxisParameter.MAX_ENDSTOP_CONF_OFFSET, 0.25)
        self.set_axis_parameter(AxisParameter.MAX_ENDSTOP_CONF_ENABLE, True)
        self.set_axis_parameter(AxisParameter.MAX_ENDSTOP_CONF_DEBONUNCE_MS, 50.0)


    def set_enable_min_endstop(self, value_b):
        self.set_axis_parameter(AxisParameter.MIN_ENDSTOP_CONF_ENABLE, value_b)

    def __read_axis_err(self):
        return self.read_axis_parameter(AxisParameter.ERROR)
    
    def __read_aixs_motor_err(self):
        return self.read_axis_parameter(AxisParameter.ERROR_MOTOR)
    
    def __read_axis_controller_err(self):
        return self.read_axis_parameter(AxisParameter.ERROR_CONTROLLER)

    def wait_to_idel(self):
        no_change_counter = 0
        last_state = None
        while self.read_motor_current_state() != AxisState.IDLE.value:
            current_state = AxisState(self.read_motor_current_state()).name
            if last_state == current_state:
                no_change_counter += 1
            sys.stdout.write('\r' + current_state + '.' * no_change_counter)
            sys.stdout.flush()
            last_state = current_state
            last_state = current_state
            time.sleep(self.__WAITING_TIME_LOOP)
        if(no_change_counter > 0): print("")

    def motor_homing(self):
        self.set_axis_parameter(AxisParameter.CONTROL_CONF_HOMING_SPEED, 2)
        self.set_axis_parameter(AxisParameter.CONTROL_CONF_REQ_STATE, AxisState.HOMING, False)

    def motor_idel(self):
        while True:
            self.set_axis_parameter(AxisParameter.CONTROL_CONF_REQ_STATE, AxisState.IDLE.value, False)
            is_idle = self.read_motor_current_state() == AxisState.IDLE.value
            print("motor state is idle: ", is_idle)
            if is_idle:
                break
            time.sleep(self.__WAITING_TIME_LOOP)

    def motor_closed_loop_control(self):
        while True:
            self.set_axis_parameter(AxisParameter.CONTROL_CONF_REQ_STATE, AxisState.CLOSED_LOOP_CONTROL.value, False)
            is_close_loop_conrol = (
                self.read_motor_current_state() == AxisState.CLOSED_LOOP_CONTROL.value
            )
            print("motor id closed loop control: ", is_close_loop_conrol)
            if is_close_loop_conrol:
                break
            time.sleep(self.__WAITING_TIME_LOOP)

    def calibration_sequence(self):
        print(AxisState(self.read_motor_current_state()).name)
        self.set_axis_parameter(AxisParameter.CONTROL_CONF_REQ_STATE, AxisState.MOTOR_CALIBRATION.value, False)
        self.wait_to_idel()

        print(AxisState(self.read_motor_current_state()).name)
        self.set_axis_parameter(AxisParameter.CONTROL_CONF_REQ_STATE, AxisState.ENCODER_INDEX_SEARCH.value, False)
        self.wait_to_idel()

        print(AxisState(self.read_motor_current_state()).name)
        self.set_axis_parameter(AxisParameter.CONTROL_CONF_REQ_STATE, AxisState.ENCODER_OFFSET_CALIBRATION.value, False)
        self.wait_to_idel()

    def read_errors(self):
        print("* Axis errors: ", AxisError(self.__read_axis_err()).name)
        print("* Axis motor errors: ", MotorError(self.__read_aixs_motor_err()).name)
        print("* Controller errors: ", ControllerError(self.__read_axis_controller_err()).name)

    def set_controller_config_position_control(self):
        self.set_axis_parameter(AxisParameter.CONTROL_CONF_CONTROL_MODE, ControlMode.POSITION_CONTROL.value)
        self.set_axis_parameter(AxisParameter.CONTROL_CONF_INPUT_MODE, InputMode.TRAP_TRAJ.value)

    def set_controlller_config_velocity_control(self):
        self.set_axis_parameter(AxisParameter.CONTROL_CONF_CONTROL_MODE, ControlMode.VELOCITY_CONTROL.value)
        self.set_axis_parameter(AxisParameter.CONTROL_CONF_INPUT_MODE, InputMode.VEL_RAMP.value)

    def set_controller_config_control_torque_mode(self):
        self.set_axis_parameter(AxisParameter.CONTROL_CONF_CONTROL_MODE, ControlMode.TORQUE_CONTROL.value)
        self.set_axis_parameter(AxisParameter.CONTROL_CONF_INPUT_MODE, InputMode.PASSTHROUGH.value)


    def read_estimate_position(self):
        return self.__axis.encoder.pos_estimate

    def read_estimate_velocity(self):
        return self.__axis.encoder.vel_estimate

    def set_position(self, position):
        self.__axis.controller.input_pos = position

    def set_velocity(self, value):
        self.__axis.controller.input_vel = value

    def set_torque(self, torque):
        self.__axis.controller.input_torque = torque # 0.0 - 1.0

    def read_motor_current_state(self):
        return self.__axis.current_state
    
    def read_motor_minstop_state(self):
        if(self.__axis.min_endstop.endstop_state):
            self.__axis.error = 0
            return True
        else:
            return False
