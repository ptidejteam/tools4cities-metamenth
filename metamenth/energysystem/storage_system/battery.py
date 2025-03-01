from metamenth.energysystem.storage_system.immobile_storage_energy_system import ImmobileStorageEnergySystem
from metamenth.enumerations import MeasurementUnit
from metamenth.enumerations import EnergySource
from metamenth.enumerations import BatteryTech


class Battery(ImmobileStorageEnergySystem):
    def __init__(self, name: str, inverter: bool, unit: MeasurementUnit,
                 energy_source: EnergySource, tech: BatteryTech):
        super().__init__(name, inverter, unit, energy_source, tech)

    def __str__(self):
        return (
            f"Battery("
            f"{super().__str__()})"
        )
