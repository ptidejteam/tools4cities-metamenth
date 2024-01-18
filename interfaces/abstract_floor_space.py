from typing import List
from .abstract_space import AbstractSpace
from datatypes import BinaryMeasure
from abc import abstractmethod
from typing import Type


class AbstractFloorSpace(AbstractSpace):
    """
    An abstract class for spaces on a floor

    Author: Peter Yefi
    Email: peteryefi@gmail.com
    """

    def __init__(self, area: Type[BinaryMeasure], location: str = None):
        super().__init__(area, location)
        self.adjacent_spaces: List[AbstractFloorSpace] = []

    @abstractmethod
    def add_adjacent_space(self, space: 'AbstractFloorSpace'):
        self.adjacent_spaces.append(space)
