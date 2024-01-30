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

    def __init__(self, area: AbstractMeasure, location: str = None):
        super().__init__(area, location)
        self._adjacent_spaces: List[AbstractFloorSpace] = []
        self._transducers: List[AbstractTransducer] = []

    @property
    def adjacent_spaces(self) -> List['AbstractFloorSpace']:
        return self._adjacent_spaces

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
        self.adjacent_spaces.append(space)

    def add_transducer(self, new_transducer: AbstractTransducer):
        """
        Adds sensors and/or actuators to entities (rooms, open spaces, equipment, etc.)
        :param new_transducer: a transducer to be added to this space
        :return:
        """
        EntityInsert.insert_space_entity(self, new_transducer, BuildingEntity.TRANSDUCER.value)

    def remove_transducer(self, name: str):
        EntityRemover.remove_space_entity(self, BuildingEntity.TRANSDUCER.value, name)

    def __str__(self) -> str:
        return (
            f"{super().__str__()}"
            f"Adjacent Spaces: {self.adjacent_spaces}, "
            f"Transducers: {self.transducers}, "
        )
