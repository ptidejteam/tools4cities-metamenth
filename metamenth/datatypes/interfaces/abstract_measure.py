from abc import ABC
from metamenth.datatypes.measure import Measure
from metamenth.enumerations import DataMeasurementType


class AbstractMeasure(ABC):
    """
    Defines properties shared by all measures

    Author: Peter Yefi
    Email: peteryefi@gmail.com
    """
    def __init__(self, measure: Measure, measure_type: DataMeasurementType = None):
        self.measurement_unit = measure.unit
        self.measure_type = measure_type

    def __str__(self):
        return f"Unit: {self.measurement_unit.value}, " \
               f"Measure Type: {self.measure_type.value if self.measure_type is not None else self.measure_type}"
