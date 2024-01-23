from typing import List
from .abstract_space import AbstractSpace
from datatypes.binary_measure import BinaryMeasure
from abc import abstractmethod
from typing import Type
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

    def __init__(self, area: Type[BinaryMeasure], location: str = None):
        super().__init__(area, location)
        self.adjacent_spaces: List[AbstractFloorSpace] = []
        self.transducers: List[AbstractTransducer] = []

    @abstractmethod
    def add_adjacent_space(self, space: 'AbstractFloorSpace'):
        """
        specifies (adds) which spaces (room and open spaces) are adjacent to other spaces
        :param space:
        :return:
        """
        self.adjacent_spaces.append(space)

    @abstractmethod
    def add_transducer(self, new_transducer: AbstractTransducer):
        """
        Adds sensors and/or actuators to entities (rooms, open spaces, equipment, etc.)
        :param new_transducer: a transducer to be added to this space
        :return:
        """
        EntityInsert.insert_space_entity(self, new_transducer, BuildingEntity.TRANSDUCER.value)

    @abstractmethod
    def remove_transducer(self, name: str):
        EntityRemover.remove_space_entity(self, BuildingEntity.TRANSDUCER.value, name)
