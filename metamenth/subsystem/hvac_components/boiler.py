from metamenth.subsystem.hvac_components.interfaces.abstract_duct_connected_component import AbstractDuctConnectedComponent
from metamenth.enumerations import BoilerCategory
from metamenth.enumerations import PowerState


class Boiler(AbstractDuctConnectedComponent):
    def __init__(self, name: str, category: BoilerCategory, power_state: PowerState):
        """
        Models a boiler in an hvac system
        :param name: the unique name of the boiler
        :param category: the boiler category
        :param power_state: the power state of the boiler
        :
        """
        super().__init__(name)
        self._category = None
        self._power_state = None

        self.power_state = power_state
        self.category = category

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
    def category(self) -> BoilerCategory:
        return self._category

    @category.setter
    def category(self, value: BoilerCategory):
        if value is not None:
            self._category = value
        else:
            raise ValueError("category must be of type BoilerCategory")

    def __str__(self):
        return (
            f"Boiler ({super().__str__()}"
            f"Power State: {self.power_state}, "
            f"Category: {self.category})"
        )
