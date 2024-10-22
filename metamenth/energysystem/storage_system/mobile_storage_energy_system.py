from metamenth.energysystem.interfaces.abstract_energy_system import AbstractEnergySystem
from metamenth.enumerations import MeasurementUnit


class MobileStorageEnergySystem(AbstractEnergySystem):
    def __init__(self, name: str, inverter: bool, unit: MeasurementUnit):
        super().__init__(name, inverter, unit)
