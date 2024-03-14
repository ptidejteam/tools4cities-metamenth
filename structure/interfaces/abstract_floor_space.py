from typing import List
from .abstract_space import AbstractSpace
from datatypes.interfaces.abstract_measure import AbstractMeasure
from utils import EntityRemover
from utils import EntityInsert
from measure_instruments.meter import Meter
from utils import StructureEntitySearch
from typing import Dict
from datatypes.interfaces.dynamic_entity import DynamicEntity
from enumerations import BuildingEntity
from subsystem.appliance import Appliance


class AbstractFloorSpace(AbstractSpace, DynamicEntity):
    """
    An abstract class for spaces on a floor

    Author: Peter Yefi
    Email: peteryefi@gmail.com
    """

    def __init__(self, area: AbstractMeasure, name: str, location: str = None, meter: Meter = None):
        """
        Models spaces on a building's floor
        :param area: the area of the space
        :param name: the name of the space
        :param location: the what3word location of the space
        """
        AbstractSpace.__init__(self, area, location)
        DynamicEntity.__init__(self)

        self._name = None
        self._adjacent_spaces: List[AbstractFloorSpace] = []
        self._meter = meter
        self._appliances: List[Appliance] = []
        # apply validation through setters
        self.name = name

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        if value is not None:
            self._name = value
        else:
            raise ValueError("name must be a string")

    @property
    def meter(self) -> Meter:
        return self._meter

    @meter.setter
    def meter(self, value: Meter):
        if value:
            if value.meter_location != self.location:
                raise ValueError("what3words location of meter should be the same as space")
        self._meter = value

    def add_adjacent_space(self, space: 'AbstractFloorSpace'):
        """
        specifies (adds) which spaces (room and open spaces) are adjacent to other spaces
        :param space:
        :return:
        """
        EntityInsert.insert_building_entity(self._adjacent_spaces, space, BuildingEntity.ADJACENT_SPACE.value)

    def remove_adjacent_space(self, adjacent_space: 'AbstractFloorSpace'):
        """
        Removes adjacent space from a space (room and open space)
        :param adjacent_space: the adjacent space to remove
        :return:
        """
        EntityRemover.remove_building_entity(self._adjacent_spaces, adjacent_space)

    def add_appliance(self, appliance: Appliance):
        """
        adds appliances to floor spaces
        :param appliance: the appliance to add
        :return:
        """
        EntityInsert.insert_building_entity(self._appliances, appliance)

    def remove_appliance(self, appliance: Appliance):
        """
        Removes appliance from a space (room and open space)
        :param appliance: the adjacent space to remove
        :return:
        """
        EntityRemover.remove_building_entity(self._appliances, appliance)

    def get_adjacent_space_by_name(self, name) -> 'AbstractFloorSpace':
        """
        Search adjacent spaces by name
        :param name: the name of the adjacent space
        :return:
        """
        return StructureEntitySearch.search_by_name(self._adjacent_spaces, name)

    def get_adjacent_space_by_uid(self, uid) -> 'AbstractFloorSpace':
        """
        Search adjacent spaces by uid
        :param uid: the unique identifier of the adjacent spaces
        :return:
        """
        return StructureEntitySearch.search_by_id(self._adjacent_spaces, uid)

    def get_adjacent_spaces(self, search_terms: Dict = None) -> ['AbstractFloorSpace']:
        """
        Search adjacent spaces by attributes values
        :param search_terms: a dictionary of attributes and their values
        :return:
        """
        return StructureEntitySearch.search(self._adjacent_spaces, search_terms)

    def get_appliance_by_name(self, name) -> Appliance:
        """
        Search appliances by name
        :param name: the name of the appliance
        :return:
        """
        return StructureEntitySearch.search_by_name(self._appliances, name)

    def get_appliance_by_uid(self, uid) -> Appliance:
        """
        Search appliance by uid
        :param uid: the unique identifier of the appliance
        :return:
        """
        return StructureEntitySearch.search_by_id(self._appliances, uid)

    def get_appliances(self, search_terms: Dict = None) -> [Appliance]:
        """
        Search appliances by attributes values
        :param search_terms: a dictionary of attributes and their values
        :return:
        """
        return StructureEntitySearch.search(self._appliances, search_terms)

    def __eq__(self, other):
        # spaces on a floor are equal if they share the same name
        if isinstance(other, AbstractFloorSpace):
            # Check for equality based on the 'name' attribute
            return self.name == other.name
        return False

    def __str__(self) -> str:
        transducers_info = "\n".join([f" - Transducer: {transducer}" for transducer in self._transducers])
        appliances_info = "\n".join([f" - Appliance: {appliance}" for appliance in self._appliances])
        spaces_info = "\n".join([f" - Adjacent Space: {space}" for space in self._adjacent_spaces])

        return (
            f"{super().__str__()}"
            f"Name: {self.name}, "
            f"Meter: {self.meter}, "
            f"Adjacent Spaces: {spaces_info}, "
            f"Transducers: {transducers_info}, "
            f"Appliances: {appliances_info}\n"
        )
