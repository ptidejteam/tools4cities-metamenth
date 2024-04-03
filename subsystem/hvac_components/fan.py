from subsystem.hvac_components.interfaces.abstract_hvac_component import AbstractHVACComponent
from enumerations import PowerState


class Fan(AbstractHVACComponent):
    def __init__(self, name: str, power_state: PowerState, vfd_ability: bool = False):
        """
        Models a fan in an hvac system
        :param name: the unique name of the heat exchanger
        :param power_state: the power state of the fan
        :param vfd_ability: indicates if the fan has variable frequency drive controller
        """
        super().__init__(name)
        self._power_state = None
        self._vfd_capability = vfd_ability

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
    def vfd_capability(self) -> bool:
        return self._vfd_capability

    @vfd_capability.setter
    def vfd_capability(self, value: bool):
        self._vfd_capability = value

    def __str__(self):
        return (
            f"Fan ({super().__str__()}"
            f"Power State: {self.power_state}, "
            f"VFD Capability : {self.vfd_capability})"
        )
