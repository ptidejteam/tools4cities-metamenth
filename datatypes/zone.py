from enumerations import ZoneType
from enumerations import HVACType
from uuid import uuid4
from typing import List
from structure.interfaces.abstract_space import AbstractSpace
from visitors import EntityRemover
from enumerations import BuildingEntity
from visitors import EntityInsert


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

    @property
    def adjacent_zones(self) -> List['Zone']:
        return self._adjacent_zones

    @property
    def overlapping_zones(self) -> List['Zone']:
        return self._overlapping_zones

    @property
    def spaces(self) -> List['AbstractSpace']:
        return self._spaces

    @spaces.setter
    def spaces(self, spaces: [AbstractSpace]):
        if spaces is not None:
            self._spaces = spaces
        else:
            raise ValueError('spaces must be of type [AbstractSpace]')

    @adjacent_zones.setter
    def adjacent_zones(self, adjacent_zones: ['Zone']):
        if adjacent_zones is not None:
            self._adjacent_zones = adjacent_zones
        else:
            raise ValueError('adjacent_zones must be of type [Zone]')

    @overlapping_zones.setter
    def overlapping_zones(self, overlapping_zones: ['Zone']):
        if overlapping_zones is not None:
            self._overlapping_zones = overlapping_zones
        else:
            raise ValueError('adjacent_zones must be of type [Zone]')

    def add_adjacent_zones(self, adjacent_zones: List['Zone']):
        """
        adds zones that are adjacent with the current zone.
        :param adjacent_zones: A list of zones that are adjacent to the current zone.
        """
        EntityInsert.insert_zonal_entity(self, adjacent_zones, BuildingEntity.ADJACENT_ZONE.value)

    def remove_zonal_entity(self, entity, UID):
        """
        Removes a zonal entity: adjacent_zone, overlapping_zone and spaces
        :param entity:
        :param UID:
        :return:
        """
        EntityRemover.remove_zonal_entity(self, entity, UID)

    def remove_overlapping_zone(self, UID):
        """
        Removes overlapping zones
        :param UID: the unique ID of the zone
        :return:
        """
        EntityRemover.remove_zonal_entity(self, BuildingEntity.OVERLAPPING_ZONE.value, UID)

    def remove_adjacent_zone(self, UID):
        """
        Removes adjacent zones
        :param UID: the unique ID of the zone
        :return:
        """
        EntityRemover.remove_zonal_entity(self, BuildingEntity.ADJACENT_ZONE.value, UID)

    def remove_space(self, UID):
        """
        Removes a space: floor, room, open space from a zone
        :param UID: the unique ID of the space entity
        :return:
        """
        EntityRemover.remove_zonal_entity(self, BuildingEntity.SPACE.value, UID)

    def add_spaces(self, spaces: List['AbstractSpace']):
        """
        Adds floors or rooms to a zone
        :param spaces: the floors and/or rooms (Abstract spaces) to be added
        """
        self.spaces.extend(spaces)

    def add_overlapping_zones(self, overlapping_zones: List['Zone']):
        """
        adds zones that overlap with the current zone.
        :param overlapping_zones: A list of zones that are overlapping with the current zone.
        """
        EntityInsert.insert_zonal_entity(self, overlapping_zones, BuildingEntity.OVERLAPPING_ZONE.value)

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
            f"Adjacent Zones Count: {len(self.adjacent_zones)}, "
            f"Overlapping Zones Count: {len(self.overlapping_zones)})"
        )

        overlapping_zones = "\n".join(str(zone) for zone in self.overlapping_zones)
        spaces = "\n".join(str(space) for space in self.spaces)
        adjacent_zones = "\n".join(str(zone) for zone in self.adjacent_zones)
        return (
            f"{zone_details}\nOverlapping Zones:\n{overlapping_zones}\n"
            f"Adjacent Zones:\n {adjacent_zones}\nSpaces: \n {spaces}"
        )
