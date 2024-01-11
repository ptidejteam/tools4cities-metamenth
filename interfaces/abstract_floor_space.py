from abc import ABC
from typing import List


class AbstractFloorSpace(ABC):
    """
    An abstract class for spaces on a floor

    Author: Peter Yefi
    Email: peteryefi@gmail.com
    """

    def __init__(self):
        self.adjacent_spaces: List[AbstractFloorSpace] = []
