from abc import ABC

from interfaces import AbstractSpace
from datatypes import BinaryMeasure
from enumerations import FloorType
from structure import OpenSpace
from structure import Room
from typing import List
from typing import Type
from measure_instruments import Meter
from visitors import EntityRemover


class Floor(AbstractSpace, ABC):
    """
    A floor on a building

    Author: Peter Yefi
    Email: peteryefi@gmail.com
    """

    def __init__(
        self,
        area: Type[BinaryMeasure],
        number: int,
        floor_type: Type[FloorType],
        description: str = None,
        open_spaces: [OpenSpace] = None,
        rooms: [Room] = None,
        location: str = None
    ):
        """
        :param area (BinaryMeasure): The area of the floor.
        :param location: The location of the floor (three words terminated with a period).
        :param description: A description of the floor.
        :param number: The floor number.
        :param floor_type: The type of floor (enum).
        :param open_spaces: Initial open spaces(s) on floor.
        :param rooms: Initial room(s) on floor.
        """
        super().__init__(area, location)
        self.area = area
        self.description = description
        self.number = number
        self.floor_type = floor_type
        self.open_spaces: List['OpenSpace'] = []
        self.rooms: List['Room'] = []
        self.meters: List['Meter'] = []

        if open_spaces:
            self.open_spaces.extend(open_spaces)

        if rooms:
            self.rooms.extend(rooms)

        # A floor should have at least one open space or one room
        if not self.open_spaces and not self.rooms:
            raise ValueError("A floor must have at least one room or one open space.")

    def add_open_spaces(self, open_spaces: List['OpenSpace']):
        """
        Add one or multiple OpenSpaces to the floor.
        :param open_spaces: The open spaces to add to the floor.
        """
        self.open_spaces.extend(open_spaces)

    def add_rooms(self, rooms: List['Room']):
        """
        Add one or multiple rooms to the floor.
        :param rooms: The open spaces to add to the floor.
        """
        self.rooms.extend(rooms)

    def add_meters(self, meters: List['Meter']):
        """
        Add one or multiple meters to the floor.
        :param meters: The open spaces to add to the floor.
        """
        self.meters.extend(meters)

    def remove_entity(self, visitor: EntityRemover, entity: str, UID: str):
        visitor.remove_floor_entity(self, entity, UID)

    def __str__(self):
        floor_details = (f"Floor {self.number} ({self.floor_type.value}): {self.description}, "
                         f"Area: {self.area}, Location: {self.location}, UID: {self.UID}, "
                         f"Rooms Count: {len(self.rooms)}, Open Spaces Count: {len(self.open_spaces)}, "
                         f"Meters Count: {len(self.meters)})")

        rooms = "\n".join(str(room) for room in self.rooms)
        open_spaces = "\n".join(str(space) for space in self.open_spaces)
        meters = "\n".join(str(meter) for meter in self.meters)

        return f"{floor_details}\nRooms:\n{rooms}\nOpen Space:\n {open_spaces}\nMeters:\n {meters}"
