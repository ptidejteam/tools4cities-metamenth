from metamenth.enumerations import MeasurementUnit
from metamenth.datatypes.binary_measure import BinaryMeasure
from metamenth.energysystem.interfaces.abstract_common_energy_system import AbstractCommonEnergySystem


class AbstractEnergySystem(AbstractCommonEnergySystem):
    def __init__(self, name: str, inverter: bool, unit: MeasurementUnit):
        super().__init__(name)
        self._inverter = None
        self._unit = None
        self._manufacturing_year = None
        self._capacity = None

        self.inverter = inverter
        self.unit = unit

    @property
    def inverter(self) -> bool:
        return self._inverter

    @inverter.setter
    def inverter(self, value: bool):
        if value is None:
            raise ValueError("inverter should be of type bool")
        self._inverter = value

    @property
    def unit(self) -> MeasurementUnit:
        return self._unit

    @unit.setter
    def unit(self, value: MeasurementUnit):
        if value is None:
            raise ValueError("unit should be of type MeasurementUnit")
        self._unit = value

    @property
    def manufacturing_year(self) -> int:
        return self._manufacturing_year

    @manufacturing_year.setter
    def manufacturing_year(self, value: int):
        if value is None:
            raise ValueError("manufacturing_year should be of type int")
        self._manufacturing_year = value

    @property
    def capacity(self) -> BinaryMeasure:
        return self._capacity

    @capacity.setter
    def capacity(self, value: BinaryMeasure):
        self._capacity = value

    def __str__(self):
        return (
            f"{super().__str__()}"
            f"Inverter: {self.inverter}, "
            f"Unit: {self.unit}, "
            f"Capacity: {self.capacity}, "
            f"Manufacturing Year: {self.manufacturing_year}, "
        )
