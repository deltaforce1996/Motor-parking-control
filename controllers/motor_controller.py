from helpers.enums import *
import time
from helpers.device_manager import DeviceManager


class MotorController(DeviceManager):
    def __init__(self, odrive_controller, axis):
        self.__odrv0 = odrive_controller.odrv0
        self.__WAITING_TIME_LOOP = 0.2
        self.__axis = getattr(self.__odrv0, axis)

    def set_init_configs(self):
        self.__axis.motor.config.pole_pairs = 7
        self.__axis.motor.config.calibration_current = 5
        self.__axis.motor.config.resistance_calib_max_voltage = 2
        self.__axis.motor.config.motor_type = MotorType.HIGH_CURRENT
        self.__axis.motor.config.current_lim = 15
        self.__axis.motor.config.requested_current_range = 20

        self.__axis.encoder.config.cpr = 2048
        self.__axis.encoder.config.bandwidth = 3000
        self.__axis.config.calibration_lockin.current = 5
        self.__axis.config.calibration_lockin.ramp_time = 0.4
        self.__axis.config.calibration_lockin.ramp_distance = 3.145927410125732
        self.__axis.config.calibration_lockin.accel = 20
        self.__axis.config.calibration_lockin.vel = 40

        self.__axis.controller.config.vel_limit = 50
        self.__axis.controller.config.pos_gain = 30
        self.__axis.controller.config.vel_gain = 0.02
        self.__axis.controller.config.vel_integrator_gain = 0.2
        self.__axis.trap_traj.config.vel_limit = 30
        self.__axis.trap_traj.config.accel_limit = 5
        self.__axis.trap_traj.config.decel_limit = 5

    def set_min_endstop(self, pin_num):
        self.__axis.min_endstop.config.gpio_num = pin_num
        self.__axis.min_endstop.config.is_active_high = False
        self.__axis.min_endstop.config.offset = -0.25
        self.__axis.min_endstop.config.enabled = True
        self.__axis.min_endstop.config.debounce_ms  = 50.0

    def set_max_endstop(self, pin_num):
        self.__axis.max_endstop.config.gpio_num = pin_num
        self.__axis.max_endstop.config.enabled = True
        self.__axis.min_endstop.config.is_active_high = False
        self.__axis.min_endstop.config.offset = -0.25
        self.__axis.min_endstop.config.debounce_ms  = 50.0

    def set_enable_min_endstop(self, value_b):
        self.__axis.min_endstop.config.enabled = value_b

    def wait_to_idel(self):
        while self.__axis.current_state != AxisState.IDLE:
            print(AxisState(self.read_motor_current_state()).name)
            time.sleep(self.__WAITING_TIME_LOOP)

    def motor_idel(self):
        while True:
            self.__axis.requested_state = AxisState.IDLE
            is_idle = self.read_motor_current_state() == AxisState.IDLE
            print("motor state is idle: ", is_idle)
            if is_idle:
                break
            time.sleep(self.__WAITING_TIME_LOOP)

    def motor_closed_loop_control(self):
        while True:
            self.__axis.requested_state = AxisState.CLOSED_LOOP_CONTROL
            is_close_loop_conrol = (
                self.read_motor_current_state() == AxisState.CLOSED_LOOP_CONTROL.value
            )
            print("motor id closed loop control: ", is_close_loop_conrol)
            if is_close_loop_conrol:
                break
            time.sleep(self.__WAITING_TIME_LOOP)

    def calibration_sequence(self):
        print(AxisState(self.__axis.current_state).name)
        self.__axis.requested_state = AxisState.MOTOR_CALIBRATION
        self.wait_to_idel()

        print(AxisState(self.__axis.current_state).name)
        self.__axis.requested_state = AxisState.ENCODER_INDEX_SEARCH
        self.wait_to_idel()

        print(AxisState(self.__axis.current_state).name)
        self.__axis.requested_state = AxisState.ENCODER_OFFSET_CALIBRATION
        self.wait_to_idel()

    def read_errors(self):
        print("* Axis errors: ", AxisError(self.__axis.error).name)
        print("* Axis motor errors: ", MotorError(self.__axis.motor.error).name)
        print("* Controller errors: ", ControllerError(self.__axis.controller.error).name)

    def set_controller_config_position_control(self):
        while True:
            self.__axis.controller.config.control_mode = ControlMode.POSITION_CONTROL
            self.__axis.controller.config.input_mode = InputMode.TRAP_TRAJ
            print(
                "Control Mode:",
                ControlMode(self.__axis.controller.config.control_mode).name,
            )
            print(
                "Input Mode:", InputMode(self.__axis.controller.config.input_mode).name
            )
            if (
                self.__axis.controller.config.control_mode
                == ControlMode.POSITION_CONTROL.value
                or self.__axis.controller.config.input_mode == InputMode.TRAP_TRAJ.value
            ):
                break
            time.sleep(self.__WAITING_TIME_LOOP)

    def set_controlller_config_velocity_control(self):
        while True:
            self.__axis.controller.config.control_mode = ControlMode.VELOCITY_CONTROL
            self.__axis.controller.config.input_mode = InputMode.PASSTHROUGH
            print(
                "Control Mode:",
                ControlMode(self.__axis.controller.config.control_mode).name,
            )
            print(
                "Input Mode:", InputMode(self.__axis.controller.config.input_mode).name
            )
            if (
                self.__axis.controller.config.control_mode
                == ControlMode.VELOCITY_CONTROL.value
                or self.__axis.controller.config.input_mode
                == InputMode.PASSTHROUGH.value
            ):
                break
            time.sleep(self.__WAITING_TIME_LOOP)

    def read_estimate_position(self):
        return self.__axis.encoder.pos_estimate

    def read_estimate_velocity(self):
        return self.__axis.encoder.vel_estimate

    def set_position(self, position):
        self.__axis.controller.input_pos = position

    def set_velocity(self, value):
        self.__axis.controller.input_vel = value

    def read_motor_current_state(self):
        return self.__axis.current_state
    
    def read_motor_minstop_state(self):
        if(self.__axis.min_endstop.endstop_state):
            self.__axis.error = 0
            return True
        else:
            return False
