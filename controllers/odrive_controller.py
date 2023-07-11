from helpers.enums import *
from helpers.device_manager import DeviceManager


class ODriveController(DeviceManager):
    def __init__(self, odrv0):
        self.odrv0 = odrv0
        self.WAITING_TIME_LOOP = 0.2
        print("Serial Number: ", self.odrv0.serial_number)
        print("Firmware: v", self.odrv0.fw_version_major,".", self.odrv0.fw_version_minor,".", self.odrv0.fw_version_revision)

    def clear_errors(self):
        self.odrv0.clear_errors()

    def read_errors(self):
        print("* ODrive errors: ", ODriveError(self.odrv0.error).name)

    def set_init_configs(self):
        self.odrv0.config.brake_resistance = 2.0
        self.odrv0.config.dc_bus_undervoltage_trip_level = 8.0
        self.odrv0.config.dc_bus_overvoltage_trip_level = 56.0
        self.odrv0.config.dc_max_positive_current = 20.0
        self.odrv0.config.dc_max_negative_current = -3.0
        self.odrv0.config.max_regen_current = 0

    def set_config_gpio_mode(self, pin_num, gpio_mode):
       gpio_name = f"gpio{pin_num}_mode"
       setattr(self.odrv0.config, gpio_name, gpio_mode)
       print(gpio_name, getattr(self.odrv0.config, gpio_name))
