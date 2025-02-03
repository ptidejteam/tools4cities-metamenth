from abc import ABC, abstractmethod
from metamenth.transducers.sensor import Sensor
from metamenth.datatypes.continuous_measure import ContinuousMeasure

class AbstractControl(ABC):

    def __init__(self, process_value_sensor: Sensor, process_actuator,
                 control_thresholds: ContinuousMeasure, run_duration: float = None):
        """
        :param process_value_sensor: the sensor for the process value to be monitored
        :param process_actuator: the actuator that execute the control decision, e.g., turn system on/off
        :param control_thresholds: the minimum and maximum values for the process value
        :param run_duration: indicates how long the control strategy will be executed. The default None value indicates
        that the strategy will execute 'forever'
        """
        self.process_value_sensor = process_value_sensor
        self.process_actuator = process_actuator
        self.control_thresholds = control_thresholds
        self.run_duration = run_duration

    @abstractmethod
    def acquire_process_value_data(self, *args, **kwargs) -> float:
        pass

    @abstractmethod
    def execute_control(self, *args, **kwargs):
        pass
