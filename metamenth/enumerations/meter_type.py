from metamenth.enumerations.abstract_enum import AbstractEnum


class MeterType(AbstractEnum):
    """
    Different types of meters used in a building.

    Author: Peter Yefi
    Email: peteryefi@gmail.com
    """
    ELECTRICITY = "Electricity"
    POWER = "Power"
    FLOW = "Flow"
    HEAT = "Heat"
    GAS = "Gas"

