class AxisParameter:
    TRAP_TRAJ_VEL_LIMIT = "trap_traj.config.vel_limit"
    TRAP_TRAJ_ACCEL_LIMIT = "trap_traj.config.accel_limit"
    TRAP_TRAJ_DECEL_LIMIT = "trap_traj.config.decel_limit"

    MOTOR_CONF_POLE_PAIRS = "motor.config.pole_pairs"
    MOTOT_CONF_CALI_CURRENT = "motor.config.calibration_current"
    MOTOT_CONF_RESISTANCE_CALI_MAX_VOLT = "motor.config.resistance_calib_max_voltage"
    MOTOR_CONF_MOTOR_TYPE = "motor.config.motor_type"
    MOTOR_CONF_CURRENT_LIMIT = "motor.config.current_lim"
    MOTOR_CONF_REQ_CURRENT_RANGE = "motor.config.requested_current_range"
    MOTOR_CONF_TORQ_CONST = "motor.config.torque_constant"

    MOTOR_CURRENT_STATE = "current_state"

    ENCODER_CONF_CPR = "encoder.config.cpr"
    ENCODER_CONF_BAND_WIDTH = "encoder.config.bandwidth"

    CONF_CALI_LOCK_CURRENT = "config.calibration_lockin.current"
    CONF_CALI_LOCK_RAMP_TIME = "config.calibration_lockin.ramp_time"
    CONF_CALI_LOCK_RAMP_DISTANCE = "config.calibration_lockin.ramp_distance"
    CONF_CALI_LOCK_ACCEL = "config.calibration_lockin.accel"
    CONF_CALI_LOCK_VEL = "config.calibration_lockin.vel"

    CONTROL_CONF_VEL_LIMIT = "controller.config.vel_limit"
    CONTROL_CONF_POS_GAIN = "controller.config.pos_gain"
    CONTROL_CONF_VEL_GAIN = "controller.config.vel_gain"
    CONTROL_CONF_VEL_INTEGRATOR_GAIN = "controller.config.vel_integrator_gain"
    CONTROL_CONF_HOMING_SPEED = "controller.config.homing_speed"
    CONTROL_CONF_REQ_STATE = "requested_state"
    CONTROL_CONF_INPUT_MODE = "controller.config.input_mode"
    CONTROL_CONF_CONTROL_MODE = "controller.config.control_mode"
    CONTROL_CONF_VEL_RAMP_RATE = "controller.config.vel_ramp_rate"

    CONTROL_INPUT_POS = "controller.input_pos"

    MIN_ENDSTOP_CONF_GPIO_NUM = "min_endstop.config.gpio_num"
    MIN_ENDSTOP_CONF_IS_ACTIVE_HIGH = "min_endstop.config.is_active_high"
    MIN_ENDSTOP_CONF_OFFSET = "min_endstop.config.offset"
    MIN_ENDSTOP_CONF_ENABLE = "min_endstop.config.enabled"
    MIN_ENDSTOP_CONF_DEBONUNCE_MS = "min_endstop.config.debounce_ms"

    MAX_ENDSTOP_CONF_GPIO_NUM = "max_endstop.config.gpio_num"
    MAX_ENDSTOP_CONF_IS_ACTIVE_HIGH = "max_endstop.config.is_active_high"
    MAX_ENDSTOP_CONF_OFFSET = "max_endstop.config.offset"
    MAX_ENDSTOP_CONF_ENABLE = "max_endstop.config.enabled"
    MAX_ENDSTOP_CONF_DEBONUNCE_MS = "max_endstop.config.debounce_ms"

    ERROR = "error"
    ERROR_MOTOR = "motor.error"
    ERROR_CONTROLLER = "controller.error"
