from datatypes import BinaryMeasure
from datatypes import LinearMeasure
from datatypes import ContinuousMeasure
from datatypes import ExponentialMeasure
from datatypes import AbstractMeasure
from datatypes import Measure


class MeasureFactory:
    @staticmethod
    def create_measure(measure_type: str, measure: Measure) -> AbstractMeasure:
        if measure_type == "binary":
            return BinaryMeasure(measure)
        elif measure_type == "linear":
            return LinearMeasure(measure)
        elif measure_type == "continuous":
            return ContinuousMeasure(measure)
        elif measure_type == "exponential":
            return ExponentialMeasure(measure)
        else:
            raise ValueError("Invalid measure type")
