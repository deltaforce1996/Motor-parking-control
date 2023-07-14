from helpers.enums import *
from helpers.device_manager import DeviceManager
import time
from helpers.odrive_params import OdriveParameter


class ODriveController(DeviceManager):
    def __init__(self, odrv0):
        self.odrv0 = odrv0
        self.WAITING_TIME_LOOP = 0.2
        print("Serial Number: ", self.odrv0.serial_number)
        print("Firmware: v", self.odrv0.fw_version_major,".", self.odrv0.fw_version_minor,".", self.odrv0.fw_version_revision)

    def clear_errors(self):
        self.odrv0.clear_errors()

    def set_odrive_parameter(self, param_name, param_value, is_check_param = True):
        attr_names = param_name.split(".")
        attr_odrive = self.odrv0

        for part in attr_names[:-1]:
            attr_odrive = getattr(attr_odrive, part)

        while True:
            setattr(attr_odrive, attr_names[-1], param_value)
            print("Set odrive param [", param_name, "] = ", param_value)
            if is_check_param:
                time.sleep(0.020)
                response = getattr(attr_odrive, attr_names[-1])
                if(round(response) == round(param_value)): break
            else:
                break
            time.sleep(self.__WAITING_TIME_LOOP)

    def read_odrive_parameter(self, param_name):
        attr_names = param_name.split('.')
        attr_odrive = self.odrv0
        for part in attr_names:
            attr_odrive = getattr(attr_odrive, part)
        print("Read odrive param [", param_name, "] = ", attr_odrive)
        return attr_odrive
    
    def __read_odrive_err(self):
        return self.read_odrive_parameter(OdriveParameter.ERROR)

    def read_errors(self):
        print("* ODrive errors: ", ODriveError(self.__read_odrive_err()).name)

    def set_init_configs(self):
        self.set_odrive_parameter(OdriveParameter.CONF_BRAKE_RESISTANCE, 2.0)
        self.set_odrive_parameter(OdriveParameter.CONF_DC_BUS_UNDER_VOLT_TRIP_LEVEL, 8.0)
        self.set_odrive_parameter(OdriveParameter.CONF_DC_BUS_OVER_VOLT_TRIP_LEVEL, 56.0)
        self.set_odrive_parameter(OdriveParameter.CONF_DC_MAX_POSITIVE_CURR, 20.0)
        self.set_odrive_parameter(OdriveParameter.CONF_DC_MAX_NEGATIVE_CURR, -3.0)
        self.set_odrive_parameter(OdriveParameter.CONF_MAX_REGEN_CURR, 0)

    def set_config_gpio_mode(self, pin_num, gpio_mode):
       gpio_name = f"gpio{pin_num}_mode"
       setattr(self.odrv0.config, gpio_name, gpio_mode)
       print(gpio_name, getattr(self.odrv0.config, gpio_name))

    def reset_config(self):
        self.odrv0.erase_configuration()
