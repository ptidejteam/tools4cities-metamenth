from metamenth.enumerations.abstract_enum import AbstractEnum


class HeatSource(AbstractEnum):
    """
    Heat source for heat pumps

    Author: Peter Yefi
    Email: peteryefi@gmail.com
    """
    AMBIENT_AIR = "AmbientAir"
    EXHAUST_AIR = "ExhaustAir"
    HORIZONTAL_GROUND_COLLECTOR = "HorizontalGroundCollector"
    VERTICAL_GROUND_COLLECTOR = "VerticalGroundCollector"
    WATER_WITH_ANTIFREEZE = "WaterWithAntiFreeze"
    AQUIFER = "Aquifer"
    OTHER = "Other"
