from typing import List
from .abstract_space import AbstractSpace
from datatypes import BinaryMeasure
from abc import abstractmethod
from typing import Type
from transducer import AbstractTransducer
from visitors import EntityRemover
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
        existing_transducer = next(
            (transducer for transducer in self.transducers if transducer.name == new_transducer.name),
            None
        )

        if existing_transducer is None:
            self.transducers.append(new_transducer)

    @abstractmethod
    def remove_transducer(self, name: str):
        EntityRemover.remove_space_entity(self, BuildingEntity.TRANSDUCER.value, name)
