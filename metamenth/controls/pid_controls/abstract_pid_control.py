"""
Copyright (c) 2023-2025 Peter Yefi.
All rights reserved. This program and the accompanying materials
are made available under the terms of the GNU General Public License v3.0
which accompanies this distribution, and is available at:
https://www.gnu.org/licenses/gpl-3.0.html

Contributors:
    Peter Yefi - API design and implementation
"""

from abc import abstractmethod
from metamenth.transducers.sensor import Sensor
from metamenth.transducers.actuator import Actuator
from metamenth.datatypes.continuous_measure import ContinuousMeasure
from metamenth.controls.abstract_control import AbstractControl

class AbstractPIDControl(AbstractControl):

    def __init__(self, process_value_sensor: Sensor, process_actuator: Actuator,
                 control_thresholds: ContinuousMeasure, run_duration: float = None):
        super().__init__(process_value_sensor, process_actuator, control_thresholds, run_duration)



    @abstractmethod
    def acquire_process_value_data(self) -> float:
        """
        This method executes periodically based on the data frequency defined
        by the process value sensor. It retrieves the process values for control decisions
        :return: the process value, e.g., temperature, relative humidity
        """
        pass

    @abstractmethod
    def execute_control(self, process_value: float):
        """
        Generates proportional, integral and derivative constants for PID loops
        (Optionally) include API request to update PID values in BMS
        :param process_value: the process value being monitored
        """
        pass
