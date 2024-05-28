from energysystem.storage_system.immobile_storage_energy_system import ImmobileStorageEnergySystem
from enumerations import MeasurementUnit
from enumerations import EnergySource
from enumerations import CapacitorTech


class SuperCapacitor(ImmobileStorageEnergySystem):
    def __init__(self, name: str, inverter: bool, unit: MeasurementUnit,
                 energy_source: EnergySource, tech: CapacitorTech):
        super().__init__(name, inverter, unit, energy_source)
        self._technology = None

    @property
    def technology(self) -> CapacitorTech:
        return self._technology

    @technology.setter
    def technology(self, value: CapacitorTech):
        if value is None:
            raise ValueError("technology should be of type CapacitorTechnology")
        self._technology = value

    def __str__(self):
        return (
            f"SuperCapacitor("
            f"{super().__str__()}, "
            f"Technology: {self.technology.value})"
        )
