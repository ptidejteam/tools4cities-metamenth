from metamenth.structure.interfaces.abstract_floor_space import AbstractFloorSpace
from metamenth.datatypes.interfaces.abstract_measure import AbstractMeasure
from metamenth.enumerations import OpenSpaceType


class OpenSpace(AbstractFloorSpace):
    """
    Defines an open space on a floor of a building

    Author: Peter Yefi
    Email: peteryefi@gmail.com
    """

    def __init__(self, name: str, area: AbstractMeasure, space_type: OpenSpaceType, location: str = None):
        """
        :param area: The area of the open space.
        :param location: The location of the open space (three words delimited with a period).
        :param space_type: The type of open space (enum).
        """
        super().__init__(area, name, location)
        self._space_type = None

        # Apply validation
        self.space_type = space_type

    @property
    def space_type(self) -> OpenSpaceType:
        return self._space_type

    @space_type.setter
    def space_type(self, value: OpenSpaceType):
        if value is None:
            raise ValueError('space_type must be of type OpenSpaceType')
        self._space_type = value

    def accept(self, visitor):
        """
        visitor method to accept
        visit operation for the current open space
        :param visitor: the visitor object
        """
        visitor.visit_open_space(self)

    def __str__(self):
        return f"OpenSpace ({super().__str__()} Space Type: {self.space_type.value})"
