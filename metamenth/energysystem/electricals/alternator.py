from metamenth.energysystem.interfaces.abstract_electrical import AbstractElectrical
from metamenth.enumerations import PowerState
from metamenth.datatypes.binary_measure import BinaryMeasure


class Alternator(AbstractElectrical):
    def __init__(self, name: str, power_state: PowerState = PowerState.NONE):
        super().__init__(name, power_state)

        self._power_rating = None

    @property
    def power_rating(self) -> BinaryMeasure:
        return self._power_rating

    @power_rating.setter
    def power_rating(self, value: BinaryMeasure):
        self._power_rating = value

    def __str__(self):
        return (
            f"Alternator("
            f"{super().__str__()}"
            f"Power Rating: {self.power_rating})"
        )

