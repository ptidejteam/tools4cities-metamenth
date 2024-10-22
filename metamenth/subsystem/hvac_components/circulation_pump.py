from metamenth.subsystem.hvac_components.interfaces.abstract_duct_connected_component import AbstractDuctConnectedComponent
from metamenth.enumerations import PowerState
from metamenth.enumerations import CirculationPumpType


class CirculationPump(AbstractDuctConnectedComponent):
    def __init__(self, name: str, pump_type: CirculationPumpType, power_state: PowerState):
        """
        Models a circulation pump in a built environment
        :param name: the unique name of the heat exchanger
        :param pump_type: the type of chiller
        :param power_state: the power state of the chiller
        """
        super().__init__(name)
        self._pump_type = None
        self._power_state = None

        self.pump_type = pump_type
        self.power_state = power_state

    @property
    def pump_type(self) -> CirculationPumpType:
        return self._pump_type

    @pump_type.setter
    def pump_type(self, value: CirculationPumpType):
        if not value:
            raise ValueError("pump_type must be of type CirculationPumpType")
        self._pump_type = value

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
            f"Circulation Pump ({super().__str__()}"
            f"Pump Type: {self._pump_type.value}, "
            f"Power State: {self.power_state.value})"
        )
