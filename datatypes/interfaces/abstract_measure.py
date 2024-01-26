from abc import ABC
from datatypes.measure import Measure
from enumerations import WeatherValueType


class AbstractMeasure(ABC):
    """
    Defines properties shared by all measures

    Author: Peter Yefi
    Email: peteryefi@gmail.com
    """
    def __init__(self, measure: Measure, measure_type: WeatherValueType = None):
        self.measurement_unit = measure.unit
        self.measure_type = measure_type

    def __str__(self):
        return f"Unit: {self.measurement_unit.value}, Measure Type: {self.measure_type.value}"
