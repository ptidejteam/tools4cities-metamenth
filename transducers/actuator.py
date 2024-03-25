from abc import ABC
from transducers.interfaces.abstract_transducer import AbstractTransducer
from measure_instruments import TriggerHistory
from typing import List
from .sensor import Sensor
from datatypes.interfaces.abstract_measure import AbstractMeasure


class Actuator(AbstractTransducer, ABC):
    """
    A representation of an actuator in a building

    Author: Peter Yefi
    Email: peteryefi@gmail.com
    """

    def __init__(self, name: str, trigger_output: object, set_point: AbstractMeasure = None,
                 trigger_input: Sensor = None, actuation_interval: float = None):
        """
        :param name: the unique name of a transducers
        :param trigger_input: the sensor whose data is associated with this trigger
        :param trigger_output: the device or equipment which is actuated
        :param set_point: the setpoint value of the actuator
        """
        super().__init__(name)
        self._set_point = None
        self._trigger_output = trigger_output
        self._trigger_input = None
        self._actuation_interval = actuation_interval

        self.set_point = set_point
        self.trigger_input = trigger_input


    @property
    def trigger_output(self) -> object:
        return self._trigger_output

    @trigger_output.setter
    def trigger_output(self, value: object):
        if value is None:
            raise ValueError('trigger_output must be of type object')
        self._trigger_output = value

    @property
    def set_point(self) -> AbstractMeasure:
        return self._set_point

    @set_point.setter
    def set_point(self, value: AbstractMeasure):
        if value is not None and self._trigger_input is not None:
            if value.measurement_unit != self._trigger_input.unit:
                raise ValueError('Input sensor measure: {} not matching set point measure: {}'
                                 .format(value.measurement_unit, self._trigger_input.unit))
        self._set_point = value

    @property
    def actuation_interval(self) -> float:
        return self._actuation_interval

    @actuation_interval.setter
    def actuation_interval(self, value: float):
        self._actuation_interval = value

    @property
    def trigger_input(self) -> Sensor:
        return self._trigger_input

    @trigger_input.setter
    def trigger_input(self, value: Sensor):
        if self._set_point is not None and value is not None:
            if self._set_point.measurement_unit != value.unit:
                raise ValueError('Input sensor measure: {} not matching set point measure: {}'
                                 .format(value.unit, self._set_point.measurement_unit))
        self._trigger_input = value

    def __str__(self):
        trigger_data = "\n".join(str(data) for data in self._data)
        return (
            f"Sensor("
            f"{super().__str__()}, "
            f"UID: {self.UID}, "
            f"Name: {self.name}, "
            f"Trigger Input: {self.trigger_input}, "
            f"Trigger Output: {self.trigger_output}, "
            f"Trigger Value: {self.actuation_interval}, "
            f"Setpoint: {self.set_point}, "
            f"Trigger Count: {len(trigger_data)}\n"
            f"Trigger History: {trigger_data})"
        )