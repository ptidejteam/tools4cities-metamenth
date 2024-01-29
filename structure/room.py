from abc import ABC
from datatypes.interfaces.abstract_measure import AbstractMeasure
from structure.interfaces.abstract_floor_space import AbstractFloorSpace
from enumerations import RoomType
from measure_instruments import Meter


class Room(AbstractFloorSpace, ABC):
    """
    Defines rooms on a floor of a building

    Author: Peter Yefi
    Email: peteryefi@gmail.com
    """

    def __init__(
        self,
        area: AbstractMeasure,
        name: str,
        room_type: RoomType,
        meter: Meter = None,
        location: str = None
    ):
        """
        :param area: The area of the room.
        :param location: The location of the room (three words terminated with a period).
        :param name: The name of the room.
        :param room_type: The type of the room.
        :param meter: if the room has any meter (optional)
        """
        super().__init__(area, location)
        self._name = None
        self._room_type = None
        self._meter = meter

        # call setters to apply validation
        self.name = name
        self.room_type = room_type

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
    def room_type(self) -> RoomType:
        return self._room_type

    @room_type.setter
    def room_type(self, value: RoomType):
        if value is not None:
            self._room_type = value
        else:
            raise ValueError("room_type must be of type RoomType")

    @property
    def meter(self) -> Meter:
        return self._meter

    @meter.setter
    def meter(self, value: Meter):
        if value:
            if value.meter_location != self.location:
                raise ValueError("what3words location of meter should be the same as room")
        self._meter = value

    def __str__(self):
        room_details = (
            f"Room ({super().__str__()} Room, "
            f"Name: {self.name}, Room Type: {self.room_type})"
        )

        if self.meter:
            room_details += f"\nAssociated Meter: {self.meter}"
        return room_details
