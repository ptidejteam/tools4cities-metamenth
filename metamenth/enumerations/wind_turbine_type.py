from metamenth.enumerations.abstract_enum import AbstractEnum


class WindTurbineType(AbstractEnum):
    """
    Types of Wind Turbine

    Author: Peter Yefi
    Email: peteryefi@gmail.com
    """
    VERTICAL_AXIS_WIND_TURBINE_ON_SHORE = "VAWTOnShore"
    HORIZONTAL_AXIS_WIND_TURBINE_ON_SHORE = "HAWTOnShore"
    VERTICAL_AXIS_WIND_TURBINE_OFF_SHORE = "VAWTOffShore"
    HORIZONTAL_AXIS_WIND_TURBINE_OFF_SHORE = "HAWTOffShore"
    OTHER = "Other"
