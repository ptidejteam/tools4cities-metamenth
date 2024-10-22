from metamenth.enumerations.abstract_enum import AbstractEnum


class OperationType(AbstractEnum):
    """
    Type of electric vehicle charging operation

    Author: Peter Yefi
    Email: peteryefi@gmail.com
    """
    CHARGING = "Charging"
    DISCHARGING = "Discharging"
