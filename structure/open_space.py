from interfaces import AbstractSpace
from interfaces import AbstractFloorSpace
from datatypes import BinaryMeasure
from enumerations import OpenSpaceType


class OpenSpace(AbstractSpace, AbstractFloorSpace):
    """
    Defines an open space on a floor of a building

    Author: Peter Yefi
    Email: peteryefi@gmail.com
    """

    def __init__(self, area: BinaryMeasure, location: str, space_type: OpenSpaceType):
        """
        Initializes an OpenSpace instance.

        Parameters:
        - area (BinaryMeasure): The area of the open space.
        - location (str): The location of the open space (three words terminated with a period).
        - space_type (OpenSpaceType): The type of open space (enum).
        """
        super().__init__(area, location)
        self.space_type = space_type

    def __str__(self):
        return (f"OpenSpace (UID: {self.UID}, Area: {self.area}, Location: {self.location}, "
                f"Space Type: {self.space_type})")