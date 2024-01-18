from typing import Type
from .abstract_range_measure import AbstractRangeMeasure
from .measure import Measure


class ContinuousMeasure(AbstractRangeMeasure):
    """
    Continuous measurement

    Author: Peter Yefi
    Email: peteryefi@gmail.com
    """

    def __init__(self, measure: Type[Measure]):
        super().__init__(measure)

    def __str__(self):
        return (
            f"ContinuousMeasure("
            f"{super().__str__()})"
        )
