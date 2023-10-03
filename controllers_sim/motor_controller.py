import time
from helpers.axis_params import AxisParameter
from helpers.enums import *
import sys

class MotorController():
    def __init__(self, odrive_controller, axis):
        self.__odrv0 = odrive_controller.odrv0
        self.__WAITING_TIME_LOOP = 0.2
        self.__axis = getattr(self.__odrv0, axis)

    def set_axis_parameter(self, param_name, param_value, is_check_param = True):
        # print("********************* Set Axis Parameter ************************")
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
                print("Respons = ", round(response))
                if(round(response) == round(param_value)): break
            else:
                break
            time.sleep(self.__WAITING_TIME_LOOP)
        # print("*****************************************************************")

    def read_axis_parameter(self, param_name):
        attr_names = param_name.split('.')
        attr_axis = self.__axis
        for part in attr_names:
            attr_axis = getattr(attr_axis, part)
        print("Read axis param [", param_name, "] = ", attr_axis)
        return attr_axis
    
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
            time.sleep(self.__WAITING_TIME_LOOP)
        if(no_change_counter > 0): print("")
    
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
            is_close_loop_conrol =  self.read_motor_current_state() == AxisState.CLOSED_LOOP_CONTROL.value 
            print("motor id closed loop control: ", is_close_loop_conrol)
            if is_close_loop_conrol:
                break
            time.sleep(self.__WAITING_TIME_LOOP)

    def motor_calibrate_control(self):
         while True:
            self.set_axis_parameter(AxisParameter.CONTROL_CONF_REQ_STATE, AxisState.MOTOR_CALIBRATION.value, False)
            is_motor_calibration =  self.read_motor_current_state() == AxisState.MOTOR_CALIBRATION.value 
            print("motor is_motor_calibration: ", is_motor_calibration)
            if is_motor_calibration:
                break
            time.sleep(self.__WAITING_TIME_LOOP)

    def motor_index_search(self):
        while True:
            self.set_axis_parameter(AxisParameter.CONTROL_CONF_REQ_STATE, AxisState.ENCODER_INDEX_SEARCH.value, False)
            index_search = self.read_motor_current_state() == AxisState.ENCODER_INDEX_SEARCH.value
            print("motor state is index_search: ", index_search)
            if index_search:
                break
            time.sleep(self.__WAITING_TIME_LOOP)

    def motor_index_encoder_offset(self):
        while True:
            self.set_axis_parameter(AxisParameter.CONTROL_CONF_REQ_STATE, AxisState.ENCODER_OFFSET_CALIBRATION.value, False)
            index_offset_calibration = self.read_motor_current_state() == AxisState.ENCODER_OFFSET_CALIBRATION.value
            print("motor_index_encoder_offset: ", index_offset_calibration)
            if index_offset_calibration:
                break
            time.sleep(self.__WAITING_TIME_LOOP)

    def read_estimate_position(self):
        return self.__axis.encoder.pos_estimate
    
    def read_trap_traj_status(self):
        return self.__axis.controller.trajectory_done

    def read_estimate_velocity(self):
        return self.__axis.encoder.vel_estimate
    
    def read_estimate_Iq_measured(self):
        return self.__axis.motor.current_control.Iq_measured

    def set_position(self, position):
        self.__axis.controller.input_pos = position

    def set_velocity(self, vel):
        self.__axis.controller.input_vel = vel

    def set_torque(self, torque):
        self.__axis.controller.input_torque = torque

    def read_motor_current_state(self):
        return self.__axis.current_state
    
    def set_controller_config_position_control(self):
        self.set_axis_parameter(AxisParameter.CONTROL_CONF_CONTROL_MODE, ControlMode.POSITION_CONTROL.value)
        self.set_axis_parameter(AxisParameter.CONTROL_CONF_INPUT_MODE, InputMode.TRAP_TRAJ.value)

    def set_controlller_config_velocity_control(self):
        self.set_axis_parameter(AxisParameter.CONTROL_CONF_CONTROL_MODE, ControlMode.VELOCITY_CONTROL.value)
        self.set_axis_parameter(AxisParameter.CONTROL_CONF_INPUT_MODE, InputMode.VEL_RAMP.value)

    def set_controller_config_control_torque_mode(self):
        self.set_axis_parameter(AxisParameter.CONTROL_CONF_CONTROL_MODE, ControlMode.TORQUE_CONTROL.value)
        self.set_axis_parameter(AxisParameter.CONTROL_CONF_INPUT_MODE, InputMode.PASSTHROUGH.value)

    def read_axis_err(self):
        return self.read_axis_parameter(AxisParameter.ERROR)
    
    def read_aixs_motor_err(self):
        return self.read_axis_parameter(AxisParameter.ERROR_MOTOR)
    
    def read_axis_controller_err(self):
        return self.read_axis_parameter(AxisParameter.ERROR_CONTROLLER)

    def read_errors(self):
        print("* Axis errors: ", AxisError(self.read_axis_err()).name)
        print("* Axis motor errors: ", MotorError(self.read_aixs_motor_err()).name)
        print("* Controller errors: ", ControllerError(self.read_axis_controller_err()).name)
        
