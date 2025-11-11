"""
Copyright (c) 2023-2025 Peter Yefi.
All rights reserved. This program and the accompanying materials
are made available under the terms of the GNU General Public License v3.0
which accompanies this distribution, and is available at:
https://www.gnu.org/licenses/gpl-3.0.html

Contributors:
    Peter Yefi - API design and implementation
"""

from abc import ABC, abstractmethod
from metamenth.transducers.sensor import Sensor
from metamenth.datatypes.continuous_measure import ContinuousMeasure
from typing import Any

class AbstractControl(ABC):

    def __init__(self, process_value_sensors: [Sensor], process_actuator,
                 control_thresholds: [ContinuousMeasure], run_duration: float = None):
        """
        :param process_value_sensors: the sensors for the process value to be monitored
        :param process_actuator: the actuator that execute the control decision, e.g., turn system on/off
        :param control_thresholds: the minimum and maximum values for the process value.
        This could be the setpoint value as well, e.g., if only the minimum value is provided
        :param run_duration: indicates how long the control strategy will be executed. The default None value indicates
        that the strategy will execute 'forever'
        """
        self.process_value_sensors = process_value_sensors
        self.process_actuator = process_actuator
        self.control_thresholds = control_thresholds
        self.run_duration = run_duration

    @abstractmethod
    def acquire_process_value_data(self, *args, **kwargs) -> Any:
        pass

    @abstractmethod
    def execute_control(self, *args, **kwargs):
        pass
