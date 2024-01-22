from abc import ABC

from datatypes import BinaryMeasure
from interfaces import AbstractFloorSpace
from enumerations import RoomType
from measure_instruments import Meter
from typing import Type


class Room(AbstractFloorSpace, ABC):
    """
    Defines rooms on a floor of a building
    """

    def __init__(
        self,
        area: Type[BinaryMeasure],
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
        self.name = name
        self.room_type = room_type
        self.meter = meter

    def __str__(self):
        room_details = (
            f"Room (UID: {self.UID}, Area: {self.area}, Location: {self.location}, "
            f"Name: {self.name}, Room Type: {self.room_type})"
        )

        if self.meter:
            room_details += f"\nAssociated Meter: {self.meter}"
        return room_details
