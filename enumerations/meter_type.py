from enum import Enum


class MeterType(Enum):
    """
    Different types of meters used in a building.

    Author: Peter Yefi
    Email: peteryefi@gmail.com
    """
    POWER = "Power"
    CHARGE_DISCHARGE = "ChargeDischarge"
    GAS = "Gas"

