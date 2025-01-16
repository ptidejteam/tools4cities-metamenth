from abc import ABC
from metamenth.transducers.interfaces.abstract_transducer import AbstractTransducer
from metamenth.subsystem.hvac_components.interfaces.abstract_hvac_component import AbstractHVACComponent
from metamenth.subsystem.hvac_components.controller import Controller
from typing import Union
from metamenth.subsystem.appliance import Appliance


class Actuator(AbstractTransducer, ABC):
    """
    A representation of an actuator in a building

    Author: Peter Yefi
    Email: peteryefi@gmail.com
    """

    def __init__(self, name: str, trigger_output: Union[AbstractHVACComponent, Appliance],
                 controller: Controller = None, actuation_interval: float = None):
        """
        :param name: the unique name of a transducers
        :param controller: the controller that triggers the actuator
        :param trigger_output: the device or equipment which is actuated
        """
        super().__init__(name)
        self._trigger_output = trigger_output
        self._controller = None
        self._actuation_interval = actuation_interval

        self.controller = controller

    @property
    def trigger_output(self) -> Union[AbstractHVACComponent, Appliance]:
        return self._trigger_output

    @trigger_output.setter
    def trigger_output(self, value: Union[AbstractHVACComponent, Appliance]):
        if value is None:
            raise ValueError('trigger_output must be of type AbstractHvACComponent or Appliance')
        self._trigger_output = value

    @property
    def actuation_interval(self) -> float:
        return self._actuation_interval

    @actuation_interval.setter
    def actuation_interval(self, value: float):
        self._actuation_interval = value

    @property
    def controller(self) -> Controller:
        return self._controller

    @controller.setter
    def controller(self, value: Controller):
        self._controller = value

    def __str__(self):
        trigger_data = "\n".join(str(data) for data in self._data)
        return (
            f"Actuator("
            f"{super().__str__()}, "
            f"UID: {self.UID}, "
            f"Name: {self.name}, "
            f"Controller: {self.controller}, "
            f"Trigger Output: {self.trigger_output}, "
            f"Trigger Value: {self.actuation_interval}, "
            f"Trigger Count: {len(trigger_data)}\n"
            f"Trigger History: {trigger_data})"
        )