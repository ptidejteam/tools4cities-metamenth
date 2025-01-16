from metamenth.controls.binary_controls.abstract_binary_control import AbstractBinaryControl
from metamenth.transducers.sensor import Sensor
from metamenth.transducers.actuator import Actuator
from metamenth.datatypes.continuous_measure import ContinuousMeasure
import random


class OnOffControl(AbstractBinaryControl):

    def __init__(self, process_value_sensor: Sensor, process_actuator: Actuator,
                 control_thresholds: ContinuousMeasure, run_duration: float = None):
        super().__init__(process_value_sensor, process_actuator, control_thresholds, run_duration)


    def acquire_process_value_data(self) -> float:
        """
        Generate random temperature values from -20 to 30 degree Celsius
        to test the implementation. Ideally, you will acquire the process value
        through an API call
        """
        return round(random.uniform(-20, 30))

    def execute_control(self, process_value: float):
        if process_value > self.control_thresholds.maximum:
            # turn off boiler through (external) API call
            print(f'process value of {process_value} is greater than maximum threshold of'
                  f' {self.control_thresholds.maximum}')
            print(f'Triggering process actuator to turn off boiler.')
        elif process_value < self.control_thresholds.minimum:
            # turn on heater through (external) API call
            print(f'process value of {process_value} is lesser than maximum threshold of'
                  f' {self.control_thresholds.maximum}')
            print(f'Triggering process actuator to turn on boiler.')