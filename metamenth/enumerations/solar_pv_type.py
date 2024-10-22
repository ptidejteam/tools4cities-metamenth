from metamenth.enumerations.abstract_enum import AbstractEnum


class SolarPVType(AbstractEnum):
    """
    Types of solar panels

    Author: Peter Yefi
    Email: peteryefi@gmail.com
    """
    BUILDING_INTEGRATED_PHOTOVOLTAIC = "BIPV"
    BUILDING_INTEGRATED_PHOTOVOLTAIC_THERMAL = "BIPVT"
    OTHER = "Other"
