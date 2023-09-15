import time

class ODriveController():
    def __init__(self, odrv0):
        self.odrv0 = odrv0
        self.WAITING_TIME_LOOP = 0.2
        print("Serial Number: ", self.odrv0.serial_number)
        print("Firmware: v", self.odrv0.fw_version_major,".", self.odrv0.fw_version_minor,".", self.odrv0.fw_version_revision)

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
            time.sleep(self.WAITING_TIME_LOOP)

    def read_odrive_parameter(self, param_name):
        attr_names = param_name.split('.')
        attr_odrive = self.odrv0
        for part in attr_names:
            attr_odrive = getattr(attr_odrive, part)
        print("Read odrive param [", param_name, "] = ", attr_odrive)
        return attr_odrive
    
    def clear_errors(self):
        self.odrv0.clear_errors()
        