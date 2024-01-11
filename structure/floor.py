from interfaces import AbstractSpace
from datatypes import BinaryMeasure
from enumerations import FloorType
from structure import OpenSpace
from typing import List


class Floor(AbstractSpace):
    """
    A floor on a building

    Author: Peter Yefi
    Email: peteryefi@gmail.com
    """

    def __init__(self, area: BinaryMeasure, location: str, description: str, number: int, floor_type: FloorType):
        """
        Initializes a Floor instance.

        Parameters:
        - area (BinaryMeasure): The area of the floor.
        - location (str): The location of the floor (three words terminated with a period).
        - description (str): A description of the floor.
        - number (int): The floor number.
        - floor_type (FloorType): The type of floor (enum).
        """
        super().__init__(area, location)
        self.description = description
        self.number = number
        self.floor_type = floor_type
        self.open_spaces: List[OpenSpace] = []

    def add_open_space(self, open_spaces: [OpenSpace]):
        """
        Add one or multiple OpenSpaces to the floor.
        Parameters:
        - open_spaces (BinaryMeasure): The open spaces to add to the floor.
        """
        self.open_spaces.extend(open_spaces)

    def __str__(self):
        floor_details = (f"Floor {self.number} ({self.floor_type.value}): {self.description}, "
                         f"Area: {self.area}, Location: {self.location}, UID: {self.UID}")

        open_space_details = "\n".join(str(space) for space in self.open_spaces)

        return f"{floor_details}\nOpen Spaces:\n{open_space_details}"
