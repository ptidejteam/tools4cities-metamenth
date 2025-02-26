from metamenth.controls.pid_controls.abstract_pid_control import AbstractPIDControl
from metamenth.transducers.sensor import Sensor
from metamenth.transducers.actuator import Actuator
from metamenth.datatypes.continuous_measure import ContinuousMeasure
import random
import numpy as np


class ZieglerNicholsTuner(AbstractPIDControl):

    def __init__(self, process_value_sensor: Sensor, process_actuator: Actuator,
                 control_thresholds: ContinuousMeasure, run_duration: float = None):
        super().__init__(process_value_sensor, process_actuator, control_thresholds, run_duration)
        self._proces_values = []
        self._errors = []
        self._optimum_data_points = 100 # number of process values to initiate Nichols Ziegler fine tuner
        self.proportional = None
        self.integral = None
        self.derivative = None


    def acquire_process_value_data(self) -> float:
        """
        Generate random temperature values from -20 to 30 degree Celsius
        to test the implementation. Ideally, you will acquire the process value
        through an API call
        """
        return round(random.uniform(10, 15))

    def execute_control(self, process_value: float):
        error = self.control_thresholds.minimum - process_value
        self._errors.append(error)
        self._proces_values.append(process_value)

        # initiate fine tuner when the accumulated data point reaches 100 or multiple of it (e.g., 200, 300, etc.)
        if len(self._proces_values) % self._optimum_data_points == 0:
            kp_values = np.linspace(0.1, 10, self._optimum_data_points)  # Range of Kp values to test
            candidate_gains = []

            for i in range(self._optimum_data_points):
                '''if np.any(np.abs(self._errors) > self.control_thresholds.minimum * 1.5):  # Check for instability
                    continue'''
                test_errors = np.array(self._errors) * kp_values[i] # Simulate the effect of kp scaling errors
                oscillations = np.diff(np.sign(test_errors))
                periods = np.where(oscillations != 0)[0]

                if len(periods) > 1:
                    period = np.mean(np.diff(periods)) * self.process_value_sensor.data_frequency
                    candidate_gains.append((kp_values[i], period, len(periods)))

            if candidate_gains:
                candidate_gains.sort(key=lambda x: (-x[2], x[1]))   # Sort by lowest period, highest oscillations
                ultimate_gain, ultimate_period, _ = candidate_gains[0]

                self.proportional = 0.6 * ultimate_gain
                self.integral = (2 * self.proportional) / ultimate_period
                self.derivative = (self.proportional * ultimate_period) / 8

                print(f'acquired {self._optimum_data_points} data points, computing ultimate gain and period')
                print(f'ultimate gain: {ultimate_gain}, ultimate period: {ultimate_period}')
            else:
                print("Tuning failed: No valid ultimate gain or period found.")

