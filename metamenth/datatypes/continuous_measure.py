from metamenth.datatypes.interfaces.abstract_range_measure import AbstractRangeMeasure
from metamenth.datatypes.measure import Measure


class ContinuousMeasure(AbstractRangeMeasure):
    """
    Continuous measurement

    Author: Peter Yefi
    Email: peteryefi@gmail.com
    """

    def __init__(self, measure: Measure):
        super().__init__(measure)

    def __str__(self):
        return (
            f"ContinuousMeasure("
            f"{super().__str__()})"
        )
