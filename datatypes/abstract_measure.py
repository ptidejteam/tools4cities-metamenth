from typing import Type
from abc import ABC
from .measure import Measure


class AbstractMeasure(ABC):
    """
    Defines properties shared by all measures

    Author: Peter Yefi
    Email: peteryefi@gmail.com
    """
    def __init__(self, measure: Type[Measure]):
        self.measurement_unit = measure.unit

    def __str__(self):
        return f"Unit: {self.measurement_unit.value}"
