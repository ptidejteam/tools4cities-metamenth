from interfaces import AbstractFloorSpace
from datatypes import BinaryMeasure
from enumerations import OpenSpaceType
from typing import Type


class OpenSpace(AbstractFloorSpace):
    """
    Defines an open space on a floor of a building

    Author: Peter Yefi
    Email: peteryefi@gmail.com
    """

    def __init__(self, area: Type[BinaryMeasure], space_type: OpenSpaceType, location: str = None):
        """
        :param area: The area of the open space.
        :param location: The location of the open space (three words delimited with a period).
        :param space_type: The type of open space (enum).
        """
        super().__init__(area, location)
        self.space_type = space_type

    def __str__(self):
        return (f"OpenSpace (UID: {self.UID}, Area: {self.area}, Location: {self.location}, "
                f"Space Type: {self.space_type})")