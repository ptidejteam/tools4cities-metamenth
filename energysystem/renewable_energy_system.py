from energysystem.interfaces.abstract_energy_system import AbstractEnergySystem
from datatypes.binary_measure import BinaryMeasure
from enumerations import MeasurementUnit


class RenewableEnergySystem(AbstractEnergySystem):
    def __init__(self, name: str, inverter: bool, unit: MeasurementUnit,  power_capacity: BinaryMeasure = None):
        super().__init__(name, inverter, unit)
        self._power_capacity = power_capacity

    @property
    def power_capacity(self) -> BinaryMeasure:
        return self._power_capacity

    @power_capacity.setter
    def power_capacity(self, value: BinaryMeasure):
        self._power_capacity = value

    def __str__(self):
        return (
            f"UID: {super().__str__()}, "
            f"Power Capacity: {self.power_capacity}, "
        )
