from dataclasses import dataclass
from metamenth.enumerations import MeasurementUnit


@dataclass
class Measure:
    unit: MeasurementUnit = None
    minimum: float = 0.0
    maximum: float = 0.0
    slope: float = 0.0
    exponent: float = 0.0
    mantissa: float = 0.0
