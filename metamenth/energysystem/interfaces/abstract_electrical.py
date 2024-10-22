from metamenth.enumerations import PowerState
from metamenth.energysystem.interfaces.abstract_common_energy_system import AbstractCommonEnergySystem


class AbstractElectrical(AbstractCommonEnergySystem):

    def __init__(self,  name: str, power_state: PowerState):
        super().__init__(name)
        self._power_state = None

        self.power_state = power_state

    @property
    def power_state(self) -> PowerState:
        return self._power_state

    @power_state.setter
    def power_state(self, value: PowerState):
        if value is None:
            raise ValueError('power_state must be on type PowerState')
        self._power_state = value

    def __str__(self):
        return (
            f"{super().__str__()}"
            f"Power State: {self.power_state}, "
        )