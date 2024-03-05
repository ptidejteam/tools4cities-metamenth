from datatypes.interfaces.abstract_measure import AbstractMeasure
from .measure import Measure
from enumerations import WeatherValueType


class BinaryMeasure(AbstractMeasure):
    """
    Represents a binary measure with a value and a measurement unit.

    Author: Peter Yefi
    Email: peteryefi@gmail.com
    """
    def __init__(self, measure: Measure, weather_type: WeatherValueType = None):
        super().__init__(measure, weather_type)
        self.value = measure.minimum

    def __str__(self):
        return (
            f"BinaryMeasure("
            f"Value: {self.value}, "
            f"{super().__str__()})"
        )
