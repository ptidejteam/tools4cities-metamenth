from dataclasses import dataclass
from enumerations import MeasurementUnit
from typing import Type


@dataclass
class Measure:
    unit: Type[MeasurementUnit] = None
    minimum: float = 0.0
    maximum: float = 0.0
    slope: float = 0.0
    exponent: float = 0.0
    mantissa: float = 0.0
