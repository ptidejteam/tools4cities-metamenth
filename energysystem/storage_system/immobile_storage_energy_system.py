from energysystem.interfaces.abstract_energy_system import AbstractEnergySystem
from energysystem.renewable_energy_system import RenewableEnergySystem
from enumerations import MeasurementUnit
from enumerations import EnergySource
from utils import EntityInsert
from utils import StructureEntitySearch
from enumerations import BuildingEntity
from enumerations import BatteryTech
from enumerations import CapacitorTech
from typing import Union


class ImmobileStorageEnergySystem(AbstractEnergySystem):
    def __init__(self, name: str, inverter: bool, unit: MeasurementUnit, energy_source: EnergySource,
                 tech: Union[BatteryTech, CapacitorTech]):
        super().__init__(name, inverter, unit)
        self._energy_source = None
        self._technology = None
        self._renewable_sources: [RenewableEnergySystem] = []

        self.energy_source = energy_source
        self.technology = tech

    @property
    def energy_source(self) -> EnergySource:
        return self._energy_source

    @energy_source.setter
    def energy_source(self, value: EnergySource):
        if value is None:
            raise ValueError("energy_source should be of type EnergySource")
        self._energy_source = value

    @property
    def technology(self) -> Union[BatteryTech, CapacitorTech]:
        return self._technology

    @technology.setter
    def technology(self, value: Union[BatteryTech, CapacitorTech]):
        if value is None:
            raise ValueError("technology should be of type CapacitorTech or BatteryTech")
        self._technology = value

    def add_renewable_energy_source(self, renewable_energy_source: RenewableEnergySystem):
        """
        adds renewable energy source for storage system
        :param renewable_energy_source: The renewable energy source
        """
        EntityInsert.insert_building_entity(self._renewable_sources, renewable_energy_source,
                                            BuildingEntity.ENERGY_SYSTEM.value)

    def get_renewable_energy_source(self, name) -> RenewableEnergySystem:
        """
        Search renewable energy source by name
        :param name:  the name of the renewable energy source
        :return:
        """
        return StructureEntitySearch.search_by_name(self._renewable_sources, name)

    def __str__(self):
        return (
            f"{super().__str__()}, "
            f"Energy Source: {self.energy_source.value}, "
            f"Technology: {self.technology.value}, "
            f"Renewal Sources: {self._renewable_sources}"
        )
