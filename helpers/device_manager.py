from abc import ABC, abstractmethod

class DeviceManager(ABC):

    def clear_errors(self):
        pass

    @abstractmethod
    def read_errors(self):
        pass

    @abstractmethod
    def set_init_configs(self):
        pass