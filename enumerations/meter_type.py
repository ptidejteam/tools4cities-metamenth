from enumerations.abstract_enum import AbstractEnum


class MeterType(AbstractEnum):
    """
    Different types of meters used in a building.

    Author: Peter Yefi
    Email: peteryefi@gmail.com
    """
    ELECTRICITY = "Electricity"
    CHARGE_DISCHARGE = "ChargeDischarge"
    FLOW = "Flow"
    HEAT = "Heat"
    GAS = "Gas"

