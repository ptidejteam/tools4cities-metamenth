from datatypes.interfaces import AbstractMeasure
from .measure import Measure


class BinaryMeasure(AbstractMeasure):
    """
    Represents a binary measure with a value and a measurement unit.

    Author: Peter Yefi
    Email: peteryefi@gmail.com
    """
    def __init__(self, measure: Measure):
        super().__init__(measure)
        self.value = measure.minimum

    def __str__(self):
        return (
            f"BinaryMeasure("
            f"Value: {self.value}, "
            f"{super().__str__()})"
        )
