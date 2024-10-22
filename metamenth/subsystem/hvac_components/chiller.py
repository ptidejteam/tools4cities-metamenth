from metamenth.subsystem.hvac_components.interfaces.abstract_duct_connected_component import AbstractDuctConnectedComponent
from metamenth.enumerations import ChillerType
from metamenth.enumerations import PowerState


class Chiller(AbstractDuctConnectedComponent):
    def __init__(self, name: str, chiller_type: ChillerType, power_state: PowerState):
        """
        Models a chiller in a built environment
        :param name: the unique name of the heat exchanger
        :param chiller_type: the type of chiller
        :param power_state: the power state of the chiller
        """
        super().__init__(name)
        self._chiller_type = None
        self._power_state = None

        self.chiller_type = chiller_type
        self.power_state = power_state

    @property
    def chiller_type(self) -> ChillerType:
        return self._chiller_type

    @chiller_type.setter
    def chiller_type(self, value: ChillerType):
        if not value:
            raise ValueError("chiller_type must be of type ChillerType")
        self._chiller_type = value

    @property
    def power_state(self) -> PowerState:
        return self._power_state

    @power_state.setter
    def power_state(self, value: PowerState):
        if value is not None:
            self._power_state = value
        else:
            raise ValueError("power_state must be of type PowerState")

    def __str__(self):
        return (
            f"Chiller ({super().__str__()}"
            f"Type: {self.chiller_type.value}, "
            f"Power State: {self.power_state})"
        )
