from .abstract_range_measure import AbstractRangeMeasure
from typing import Type
from .measure import Measure


class ExponentialMeasure(AbstractRangeMeasure):
    """
    Exponential measurement

    Author: Peter Yefi
    Email: peteryefi@gmail.com
    """
    def __init__(self, measure: Type[Measure]):
        super().__init__(measure)
        self.exponent = measure.exponent
        self.mantissa: measure.mantissa

    def __str__(self):
        return (
            f"ExponentialMeasure("
            f"Exponent: {self.exponent}, "
            f"Mantissa: {self.maximum}, "
            f"{super().__str__()})"
        )