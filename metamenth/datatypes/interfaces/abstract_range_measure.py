from .abstract_measure import AbstractMeasure
from metamenth.datatypes.measure import Measure


class AbstractRangeMeasure(AbstractMeasure):
    """
    Defines properties shared by linear, continuous and exponential measures

    Author: Peter Yefi
    Email: peteryefi@gmail.com
    """

    def __init__(self, measure: Measure):
        super().__init__(measure)
        self.minimum = measure.minimum
        self.maximum = measure.maximum

    def __str__(self):
        return (
            f"Minimum: {self.minimum}, "
            f"Maximum: {self.maximum}, "
            f"{super().__str__()}"
        )
