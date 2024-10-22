from metamenth.enumerations.abstract_enum import AbstractEnum


class CirculationPumpType(AbstractEnum):
    """
    Types of circulation pumps

    Author: Peter Yefi
    Email: peteryefi@gmail.com
    """
    CENTRIFUGAL = "Centrifugal"
    CONSTANT_PRESSURE = "ConstantPressure"
    OTHER = "Other"

