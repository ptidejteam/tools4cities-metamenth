from metamenth.enumerations.abstract_enum import AbstractEnum


class DuctType(AbstractEnum):
    """
    Different types of ducts

    Author: Peter Yefi
    Email: peteryefi@gmail.com
    """
    AIR = "Air"
    WATER = "Water"
    WATER_WITH_ANTI_FREEZE = "WaterWithAntiFreeze"
    DHN = "DHN"
    OTHER = "Other"
