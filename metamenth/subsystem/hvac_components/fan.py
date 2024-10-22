from metamenth.subsystem.hvac_components.interfaces.abstract_hvac_component import AbstractHVACComponent
from metamenth.enumerations import PowerState

from metamenth.subsystem.hvac_components.variable_frequency_drive import VariableFrequencyDrive


class Fan(AbstractHVACComponent):
    def __init__(self, name: str, power_state: PowerState, vfd: VariableFrequencyDrive = None):
        """
        Models a fan in an hvac system
        :param name: the unique name of the heat exchanger
        :param power_state: the power state of the fan
        """
        super().__init__(name)
        self._power_state = None
        self._vfd = vfd
        self.power_state = power_state

    @property
    def power_state(self) -> PowerState:
        return self._power_state

    @power_state.setter
    def power_state(self, value: PowerState):
        if value is not None:
            self._power_state = value
        else:
            raise ValueError("power_state must be of type PowerState")

    @property
    def vfd(self) -> VariableFrequencyDrive:
        return self._vfd

    @vfd.setter
    def vfd(self, value: VariableFrequencyDrive):
        self._vfd = value

    def __str__(self):
        return (
            f"Fan ({super().__str__()}"
            f"VFD: {self.vfd}, "
            f"Power State: {self.power_state})"
        )
