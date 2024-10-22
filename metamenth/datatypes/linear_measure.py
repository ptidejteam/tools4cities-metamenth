from metamenth.datatypes.interfaces.abstract_range_measure import AbstractRangeMeasure
from metamenth.datatypes.measure import Measure


class LinearMeasure(AbstractRangeMeasure):
    """
    Linear measurement

    Author: Peter Yefi
    Email: peteryefi@gmail.com
    """
    def __init__(self, measure: Measure):
        """
        :param measure: the measurement object
        """
        super().__init__(measure)
        self.slope = measure.slope

    def __str__(self):
        return (
            f"LinearMeasure("
            f"Slope: {self.slope}, "
            f"{super().__str__()})"
        )

