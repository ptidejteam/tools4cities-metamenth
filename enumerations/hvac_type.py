from enum import Enum


class HVACType(Enum):
    """
    Different types of HVAC (Thermal) Zones.

    Author: Peter Yefi
    Email: peteryefi@gmail.com
    """
    PERIMETER = "Perimeter"
    INTERIOR = "Interior"
    NONE = None
