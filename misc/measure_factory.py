from datatypes.binary_measure import BinaryMeasure
from datatypes.linear_measure import LinearMeasure
from datatypes.continuous_measure import ContinuousMeasure
from datatypes.exponential_measure import ExponentialMeasure
from datatypes.interfaces import AbstractMeasure
from datatypes.measure import Measure


class MeasureFactory:
    """
    A factory class that returns various types of measures
    """
    @staticmethod
    def create_measure(measure_type: str, measure: Measure) -> AbstractMeasure:
        if measure_type == "Binary":
            return BinaryMeasure(measure)
        elif measure_type == "Linear":
            return LinearMeasure(measure)
        elif measure_type == "Continuous":
            return ContinuousMeasure(measure)
        elif measure_type == "Exponential":
            return ExponentialMeasure(measure)
        else:
            raise ValueError("Invalid measure type")
