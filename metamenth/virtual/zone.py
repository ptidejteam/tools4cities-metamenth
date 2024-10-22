from metamenth.enumerations import ZoneType
from metamenth.enumerations import HVACType
from uuid import uuid4
from typing import List
from metamenth.structure.interfaces.abstract_space import AbstractSpace
from metamenth.utils import EntityRemover
from metamenth.enumerations import BuildingEntity
from metamenth.utils import EntityInsert
from metamenth.utils import StructureEntitySearch
from metamenth.utils import StructureSearch
from typing import Dict


class Zone:
    """
    A zone in a building e.g. HVAC (thermal) zone

    Author: Peter Yefi
    Email: peteryefi@gmail.com
    """

    def __init__(self,
                 name: str,
                 zone_type: ZoneType,
                 hvac_type: HVACType = HVACType.NONE,
                 description: str = None
                 ):
        """
        :param name: The name of the zone
        :param description: The description of the zone.
        :param zone_type: The type of the zone.
        :param hvac_type: The HVAC type of the zone. Defaults to HVACType.NONE if zone_type is not HVAC.
        """
        self._UID = str(uuid4())
        self._description = description
        self._name = None
        self._zone_type = None
        self._hvac_type = None
        self._adjacent_zones: List['Zone'] = []
        self._overlapping_zones: List['Zone'] = []
        self._spaces: List['AbstractSpace'] = []

        # Apply validation
        self.name = name
        self.zone_type = zone_type
        if zone_type == ZoneType.HVAC:
            self.hvac_type = hvac_type

    @property
    def UID(self) -> str:
        return self._UID

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, value: str):
        self._description = value

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        if value is None:
            raise ValueError('name must be a string')
        self._name = value

    @property
    def zone_type(self) -> ZoneType:
        return self._zone_type

    @zone_type.setter
    def zone_type(self, value: ZoneType):
        if value is None:
            raise ValueError('zone_type must be of type ZoneType')
        self._zone_type = value

    @property
    def hvac_type(self) -> HVACType:
        return self._hvac_type

    @hvac_type.setter
    def hvac_type(self, value: ZoneType):
        if self.zone_type != ZoneType.HVAC:
            raise ValueError("HVAC type is only applicable for zones with ZoneType.HVAC.")
        self._hvac_type = value

    def add_adjacent_zones(self, adjacent_zones: List['Zone']):
        """
        adds zones that are adjacent with the current zone.
        :param adjacent_zones: A list of zones that are adjacent to the current zone.
        """
        EntityInsert.insert_building_entity(self._adjacent_zones, adjacent_zones, BuildingEntity.ADJACENT_ZONE.value, self)

    def remove_overlapping_zone(self, overlapping_zone: 'Zone'):
        """
        Removes overlapping zones
        :param overlapping_zone: the overlapping zone to remove
        :return:
        """
        EntityRemover.remove_building_entity(self._overlapping_zones, overlapping_zone,
                                             BuildingEntity.OVERLAPPING_ZONE.value, self)

    def remove_adjacent_zone(self, adjacent_zone: 'Zone'):
        """
        Removes adjacent zones
        :param adjacent_zone: the adjacent zone to remove
        :return:
        """
        EntityRemover.remove_building_entity(self._adjacent_zones, adjacent_zone,
                                             BuildingEntity.ADJACENT_ZONE.value, self)

    def remove_space(self, space: AbstractSpace):
        """
        Removes a space: floor, room, open space from a zone
        :param space: the space to remove
        :return:
        """
        EntityRemover.remove_building_entity(self._spaces, space)

    def add_spaces(self, spaces: List['AbstractSpace']):
        """
        Adds floors or rooms to a zone
        :param spaces: the floors and/or rooms (Abstract spaces) to be added
        """
        EntityInsert.insert_building_entity(self._spaces, spaces,
                                            BuildingEntity.FLOOR_SPACE.value)

    def add_overlapping_zones(self, overlapping_zones: List['Zone']):
        """
        adds zones that overlap with the current zone.
        :param overlapping_zones: A list of zones that are overlapping with the current zone.
        """
        EntityInsert.insert_building_entity(self._overlapping_zones, overlapping_zones,
                                            BuildingEntity.OVERLAPPING_ZONE.value, self)

    def get_adjacent_zone_by_name(self, name) -> 'Zone':
        """
        Search adjacent zones by name
        :param name:  the name of the zone
        :return:
        """
        return StructureEntitySearch.search_by_name(self._adjacent_zones, name)

    def get_adjacent_zone_by_uid(self, uid) -> 'Zone':
        """
        Search adjacent zones by uid
        :param uid: the unique identifier of the adjacent zone
        :return:
        """
        return StructureEntitySearch.search_by_id(self._adjacent_zones, uid)

    def get_adjacent_zones(self, search_terms: Dict = None) -> ['Zone']:
        """
        Search adjacent zones by attributes values
        :param search_terms: a dictionary of attributes and their values
        :return:
        """
        return StructureEntitySearch.search(self._adjacent_zones, search_terms)

    def get_overlapping_zone_by_name(self, name) -> 'Zone':
        """
        Search overlapping zones by name
        :param name:  the name of the zone
        :return:
        """
        return StructureEntitySearch.search_by_name(self._overlapping_zones, name)

    def get_overlapping_zone_by_uid(self, uid) -> 'Zone':
        """
        Search overlapping zones by uid
        :param uid: the unique identifier of the overlapping zone
        :return:
        """
        return StructureEntitySearch.search_by_id(self._overlapping_zones, uid)

    def get_overlapping_zones(self, search_terms: Dict = None) -> ['Zone']:
        """
        Search overlapping zones by attributes values
        :param search_terms: a dictionary of attributes and their values
        :return:
        """
        return StructureEntitySearch.search(self._overlapping_zones, search_terms)

    def get_space_by_uid(self, uid) -> 'AbstractSpace':
        """
        Search spaces by uid
        :param uid: the unique identifier of the space
        :return:
        """
        return StructureSearch.search_by_id(self._spaces, uid)

    def get_spaces(self, search_terms: Dict = None) -> ['AbstractSpace']:
        """
        Search spaces by attributes values
        :param search_terms: a dictionary of attributes and their values
        :return:
        """
        return StructureSearch.search(self._spaces, search_terms)

    def __eq__(self, other):
        # zones are equal if they share the same name
        if isinstance(other, Zone):
            # Check for equality based on the 'name' attribute
            return self.name == other.name
        return False

    def __str__(self):

        zone_details = (
            f"Zone("
            f"UID: {self.UID}, "
            f"Name: {self.name}, "
            f"Description: {self.description}, "
            f"ZoneType: {self.zone_type.value}, "
            f"HVACType: {self.hvac_type.value if self.hvac_type is not None else HVACType.NONE}, "
            f"Adjacent Zones Count: {len(self._adjacent_zones)}, "
            f"Overlapping Zones Count: {len(self._overlapping_zones)})"
        )

        overlapping_zones = "\n".join(str(zone) for zone in self._overlapping_zones)
        spaces = "\n".join(str(space) for space in self._spaces)
        adjacent_zones = "\n".join(str(zone) for zone in self._adjacent_zones)
        return (
            f"{zone_details}\nOverlapping Zones:\n{overlapping_zones}\n"
            f"Adjacent Zones:\n {adjacent_zones}\nSpaces: \n {spaces}"
        )
