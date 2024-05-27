from energysystem.interfaces.abstract_energy_system import AbstractEnergySystem
from enumerations import MeasurementUnit


class NonRenewableEnergySystem(AbstractEnergySystem):
    def __init__(self, name: str, inverter: bool, unit: MeasurementUnit):
        super().__init__(name, inverter, unit)

