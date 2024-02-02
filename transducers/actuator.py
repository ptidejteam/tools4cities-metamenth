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

    def __init__(self, name: str,  set_point: AbstractMeasure, trigger_output: object, trigger_input: Sensor,
                 trigger_value: int = None):
        """
        :param name: the unique name of a transducers
        :param trigger_input: the sensor whose data is associated with this trigger
        :param trigger_output: the device or equipment which is actuated
        :param trigger_value: value recorded by sensor that related to this actuation
        :param set_point: the setpoint value of the actuator
        """
        super().__init__(name)
        self.set_point = set_point
        self.trigger_output = trigger_output
        self.trigger_input = trigger_input
        self.trigger_value = trigger_value
        self.data: [TriggerHistory] = []

    def add_data(self, data: List[TriggerHistory]):
        """
        Adds data (record of trigger to an actuator
        :param data: the actuator trigger data to be added
        :return:
        """
        self.data.extend(data)

    def __str__(self):
        trigger_data = "\n".join(str(data) for data in self.data)
        return (
            f"Sensor("
            f"{super().__str__()}, "
            f"UID: {self.UID}, "
            f"Name: {self.name}, "
            f"Trigger Input: {self.trigger_input}, "
            f"Trigger Output: {self.trigger_output}, "
            f"Trigger Value: {self.trigger_value}, "
            f"Setpoint: {self.set_point}, "
            f"Trigger Count: {len(trigger_data)}\n"
            f"Trigger History: {trigger_data})"
        )