from metamenth.structure.interfaces.abstract_space import AbstractSpace
from metamenth.datatypes.interfaces.abstract_measure import AbstractMeasure
from metamenth.enumerations import FloorType
from metamenth.structure.open_space import OpenSpace
from metamenth.structure.room import Room
from metamenth.utils import EntityRemover
from metamenth.enumerations import BuildingEntity
from metamenth.utils import EntityInsert
from typing import Union
from metamenth.utils import StructureSearch
from typing import Dict
from typing import List


class Floor(AbstractSpace):
    """
    A floor on a building

    Author: Peter Yefi
    Email: peteryefi@gmail.com
    """

    def __init__(
        self,
        area: AbstractMeasure,
        number: int,
        floor_type: FloorType,
        height: AbstractMeasure = None,
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
        self._description = description
        self._height = height
        self._number = None
        self._floor_type = None
        self._open_spaces: List['OpenSpace'] = []
        self._rooms: List['Room'] = []

        # apply validation
        self.number = number
        self.floor_type = floor_type

        if open_spaces:
            self.add_open_spaces(open_spaces)

        if rooms:
            self.add_rooms(rooms)

        # A floor should have at least one open space or one room
        if not self._open_spaces and not self._rooms:
            raise ValueError("A floor must have at least one room or one open space.")

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, value: str):
        self._description = value

    @property
    def number(self) -> int:
        return self._number

    @number.setter
    def number(self, value: int):
        if value is not None:
            self._number = value
        else:
            raise ValueError("number must be an int")

    @property
    def floor_type(self) -> FloorType:
        return self._floor_type

    @floor_type.setter
    def floor_type(self, value: FloorType):
        if value is not None:
            self._floor_type = value
        else:
            raise ValueError("floor_type must be of type FloorType")

    @property
    def height(self) -> AbstractMeasure:
        return self._height

    @height.setter
    def height(self, value: AbstractMeasure):
        if value is not None:
            self._height = value
        else:
            raise ValueError("height must be of type AbstractMeasure")

    @property
    def open_spaces(self):
        raise AttributeError("Cannot get open_spaces")

    @open_spaces.setter
    def open_spaces(self, value: Union[OpenSpace, List[OpenSpace]]):
        if value is not None:
            if isinstance(value, list):
                self._open_spaces = value
            else:
                self._open_spaces.append(value)
        else:
            raise ValueError("open_spaces must be of type [OpenSpace]")

    @property
    def rooms(self):
        raise AttributeError("Cannot get rooms")

    @rooms.setter
    def rooms(self, value: Union[Room, List[Room]]):
        if value is not None:
            if isinstance(value, list):
                self._rooms = value
            else:
                self._rooms.append(value)
        else:
            raise ValueError("rooms must be of type [Room]")

    def add_open_spaces(self, open_spaces: List['OpenSpace']):
        """
        Add one or multiple OpenSpaces to the floor.
        :param open_spaces: The open spaces to add to the floor.
        """
        EntityInsert.insert_building_entity(self._open_spaces, open_spaces, BuildingEntity.FLOOR_SPACE.value)
        return self

    def add_rooms(self, rooms: List['Room']):
        """
        Add one or multiple rooms to the floor.
        :param rooms: The open spaces to add to the floor.
        """
        EntityInsert.insert_building_entity(self._rooms, rooms, BuildingEntity.FLOOR_SPACE.value)
        return self

    def remove_open_space(self, open_space: OpenSpace):
        """
        Removes open space from a floor
        :param open_space: the open space entity to remove
        :return:
        """
        EntityRemover.remove_building_entity(self._open_spaces, open_space, BuildingEntity.OPEN_SPACE.value, self)
        return self

    def remove_room(self, room: Room):
        """
        Removes room from a floor
        :param room: the room to remove
        :return:
        """
        EntityRemover.remove_building_entity(self._rooms, room, BuildingEntity.ROOM.value, self)

    def get_open_space_by_uid(self, uid: str) -> OpenSpace:
        """
        Retrieves an open space given the uid
        :param uid: the uid of the open space
        :return:
        """
        return StructureSearch.search_by_id(self._open_spaces, uid)

    def get_room_by_uid(self, uid: str) -> Room:
        """
        Retrieves a room given the uid
        :param uid: the uid of the room
        :return:
        """
        return StructureSearch.search_by_id(self._rooms, uid)

    def get_open_space_by_name(self, name: str) -> OpenSpace:
        """
        Retrieves an open space given the name
        :param name: the name of the open space
        :return:
        """
        return StructureSearch.search_by_name(self._open_spaces, name)

    def get_room_by_name(self, name: str) -> Room:
        """
        Retrieves a room given its name
        :param name: the name of the room
        :return:
        """
        return StructureSearch.search_by_name(self._rooms, name)

    def get_rooms(self, search_term: Dict = None) -> List[Room]:
        """
        Retrieves rooms that match attributes and their values
        :param search_term: attributes and their values
        :return:
        """
        return StructureSearch.search(self._rooms, search_term)

    def get_open_spaces(self, search_term: Dict = None) -> List[OpenSpace]:
        """
        Retrieves open spaces that match attributes and their values
        :param search_term: attributes and their values
        :return:
        """
        return StructureSearch.search(self._open_spaces, search_term)

    def accept(self, visitor):
        """
        visitor method to accept
        visit operation for the current floor
        :param visitor: the visitor object
        """
        visitor.visit_floor(self)

    def __eq__(self, other):
        # floors are equal if they share the same number
        if isinstance(other, Floor):
            # Check for equality based on the 'number' attribute
            return self.number == other.number
        return False

    def __str__(self):
        floor_details = (f"Floor {super().__str__()} {self.number} ({self.floor_type.value}): {self.description}, "
                         f"Area: {self.area}, Height: {self.height}, Location: {self.location}, UID: {self.UID}, "
                         f"Rooms Count: {len(self._rooms)}, Open Spaces Count: {len(self._open_spaces)})")

        rooms = "\n".join(str(room) for room in self._rooms)
        open_spaces = "\n".join(str(space) for space in self._open_spaces)

        return f"{floor_details}\nRooms:\n{rooms}\nOpen Space:\n {open_spaces})"
