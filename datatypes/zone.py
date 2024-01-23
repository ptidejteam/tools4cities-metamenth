from enumerations import ZoneType
from enumerations import HVACType
from uuid import uuid4
from typing import List
from structure.interfaces import AbstractSpace
from typing import Type


class Zone:
    """
    A zone in a building e.g. HVAC (thermal) zone

    Author: Peter Yefi
    Email: peteryefi@gmail.com
    """
    def __init__(self,
                 name: str,
                 zone_type: Type[ZoneType],
                 hvac_type: Type[HVACType] = HVACType.NONE,
                 description: str = None
                 ):
        """
        :param name: The name of the zone
        :param description: The description of the zone.
        :param zone_type: The type of the zone.
        :param hvac_type: The HVAC type of the zone. Defaults to HVACType.NONE if zone_type is not HVAC.
        """
        self.UID = str(uuid4())
        self.description = description
        self.name = name
        self.zone_type = zone_type
        self.hvac_type = hvac_type if zone_type == ZoneType.HVAC else HVACType.NONE
        self.adjacent_zones: List['Zone'] = []
        self.overlapping_zones: List['Zone'] = []
        self.spaces: List['AbstractSpace'] = []

    def add_adjacent_zones(self, adjacent_zones: List['Zone']):
        """
        adds zones that are adjacent with the current zone.
        :param adjacent_zones: A list of zones that are adjacent to the current zone.
        """
        for new_adjacent_zone in adjacent_zones:
            # Search for the zone with the same name in the adjacent_zones list
            existing_adjacent_zone = next((zone for zone in self.adjacent_zones if zone.name == new_adjacent_zone.name),
                                          None)
            if existing_adjacent_zone is None:
                # If not found, add the new adjacent zone to the adjacent_zones list
                self.overlapping_zones.append(new_adjacent_zone)

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
        for new_overlapping_zone in overlapping_zones:
            # Search for the zone with the same name in the overlapping_zones list
            existing_overlapping_zone = next(
                (zone for zone in self.overlapping_zones if zone.name == new_overlapping_zone.name),
                None
            )

            if existing_overlapping_zone is None:
                # If not found, add the new zone to the overlapping_zones list
                self.overlapping_zones.append(new_overlapping_zone)

    def __str__(self):

        zone_details = (
            f"Zone("
            f"UID: {self.UID}, "
            f"Description: {self.description}, "
            f"ZoneType: {self.zone_type.value}, "
            f"HVACType: {self.hvac_type.value}, "
            f"Adjacent Zones: {len(self.adjacent_zones)}, "
            f"Overlapping Zones: {len(self.overlapping_zones)})"
        )

        overlapping_zones = "\n".join(str(zone) for zone in self.overlapping_zones)
        spaces = "\n".join(str(space) for space in self.spaces)
        adjacent_zones = "\n".join(str(zone) for zone in self.adjacent_zones)
        return (
            f"{zone_details}\nOverlapping Zones:\n{overlapping_zones}\n"
            f"Adjacent Zones:\n {adjacent_zones}\nSpaces: \n {spaces}"
        )

