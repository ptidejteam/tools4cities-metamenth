from typing import List
from .abstract_space import AbstractSpace
from datatypes.interfaces.abstract_measure import AbstractMeasure
from transducer.interfaces import AbstractTransducer
from visitors import EntityRemover
from visitors import EntityInsert
from enumerations import BuildingEntity


class AbstractFloorSpace(AbstractSpace):
    """
    An abstract class for spaces on a floor

    Author: Peter Yefi
    Email: peteryefi@gmail.com
    """

    def __init__(self, area: AbstractMeasure, name: str, location: str = None):
        super().__init__(area, location)
        self._name = None
        self._adjacent_spaces: List[AbstractFloorSpace] = []
        self._transducers: List[AbstractTransducer] = []

        # apply validation through setters
        self.name = name

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
    def adjacent_spaces(self) -> List['AbstractFloorSpace']:
        return self._adjacent_spaces

    @adjacent_spaces.setter
    def adjacent_spaces(self, value: ['AbstractFloorSpace']):
        if value is not None:
            self._adjacent_spaces = value
        else:
            raise ValueError("adjacent_spaces must be of type [AbstractFloorSpace]")

    @property
    def transducers(self) -> List[AbstractTransducer]:
        return self._transducers

    @transducers.setter
    def transducers(self, value: [AbstractTransducer]):
        if value is not None:
            self._transducers = value
        else:
            raise ValueError("transducers must be of type [Transducers]")

    def add_adjacent_space(self, space: 'AbstractFloorSpace'):
        """
        specifies (adds) which spaces (room and open spaces) are adjacent to other spaces
        :param space:
        :return:
        """
        EntityInsert.insert_space_entity(self, space, BuildingEntity.ADJACENT_SPACE.value)

    def remove_adjacent_space(self, adjacent_space: 'AbstractFloorSpace'):
        """
        Removes adjacent space from a space (room and open space)
        :param adjacent_space: the adjacent space to remove
        :return:
        """
        EntityRemover.remove_space_entity(self, BuildingEntity.ADJACENT_SPACE.value, adjacent_space)

    def add_transducer(self, new_transducer: AbstractTransducer):
        """
        Adds sensors and/or actuators to entities (rooms, open spaces, equipment, etc.)
        :param new_transducer: a transducer to be added to this space
        :return:
        """
        EntityInsert.insert_space_entity(self, new_transducer, BuildingEntity.TRANSDUCER.value)

    def remove_transducer(self, transducer: AbstractTransducer):
        """
        Removes a transducer from a room or open space
        :param transducer: the transducer to remove
        :return:
        """
        EntityRemover.remove_space_entity(self, BuildingEntity.TRANSDUCER.value, transducer)

    def __eq__(self, other):
        # spaces on a floor are equal if they share the same name
        if isinstance(other, AbstractFloorSpace):
            # Check for equality based on the 'name' attribute
            return self.name == other.name
        return False

    def __str__(self) -> str:
        return (
            f"{super().__str__()}"
            f"Name: {self.name}"
            f"Adjacent Spaces: {self.adjacent_spaces}, "
            f"Transducers: {self.transducers}, "
        )
