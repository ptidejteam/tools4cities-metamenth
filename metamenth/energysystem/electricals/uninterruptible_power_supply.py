from metamenth.energysystem.interfaces.abstract_electrical import AbstractElectrical
from metamenth.enumerations import PowerState
from metamenth.enumerations import UPSPhase
from metamenth.datatypes.binary_measure import BinaryMeasure
from metamenth.energysystem.storage_system.immobile_storage_energy_system import ImmobileStorageEnergySystem
from metamenth.enumerations import BuildingEntity
from metamenth.utils import EntityInsert
from metamenth.utils import EntityRemover
from metamenth.utils import StructureEntitySearch


class UninterruptiblePowerSupply(AbstractElectrical):
    def __init__(self, name: str, power_state: PowerState, phase: UPSPhase):
        super().__init__(name, power_state)
        self._phase = None
        self._noise_filtering = False
        self._surge_suppression = False
        self._power_rating = None
        self._storage_systems: [] = [ImmobileStorageEnergySystem]

        self.phase = phase

    @property
    def phase(self) -> UPSPhase:
        return self._phase

    @phase.setter
    def phase(self, value: UPSPhase):
        if value is None:
            raise ValueError('phase should be of type UPSPhase')
        self._phase = value

    @property
    def noise_filtering(self) -> bool:
        return self._noise_filtering

    @noise_filtering.setter
    def noise_filtering(self, value: bool):
        self._noise_filtering = value

    @property
    def surge_suppression(self) -> bool:
        return self._surge_suppression

    @surge_suppression.setter
    def surge_suppression(self, value: bool):
        self._surge_suppression = value

    @property
    def power_rating(self) -> BinaryMeasure:
        return self._power_rating

    @power_rating.setter
    def power_rating(self, value: BinaryMeasure):
        self._power_rating = value

    def add_storage_system(self, storage_system: ImmobileStorageEnergySystem):
        """
        adds storage system to UPS
        :param storage_system: the storage system to add
        :return:
        """
        EntityInsert.insert_building_entity(self._storage_systems, storage_system, BuildingEntity.HVAC_COMPONENT.value)

    def remove_storage_system(self, storage_system: ImmobileStorageEnergySystem):
        """
        Removes storage system from UPS
        :param storage_system: the storage system to remove
        :return:
        """
        EntityRemover.remove_building_entity(self._storage_systems, storage_system)

    def get_storage_system_by_name(self, name) -> ImmobileStorageEnergySystem:
        """
        Search storage system by name
        :param name: the name of the storage system
        :return:
        """
        return StructureEntitySearch.search_by_name(self._storage_systems, name)

    def __str__(self):
        return (
            f"UninterruptiblePowerSupply("
            f"{super().__str__()}"
            f"Phase: {self.phase}, "
            f"Noise Filtering: {self.noise_filtering}, "
            f"Surge Suppression: {self.surge_suppression}, "
            f"Power Rating: {self.power_rating})"
        )
