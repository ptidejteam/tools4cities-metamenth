from enumerations import MeasurementUnit
from dataclasses import dataclass


@dataclass
class BinaryMeasure:
    """
    Represents a binary measure with a value and a measurement unit.

    Author: Peter Yefi
    Email: peteryefi@gmail.com
    """
    value: float = 0.0
    measurement_unit: MeasurementUnit = None
