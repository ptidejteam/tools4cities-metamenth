from enumerations.abstract_enum import AbstractEnum


class DuctSubType(AbstractEnum):
    """
    Subtypes of ducts

    Author: Peter Yefi
    Email: peteryefi@gmail.com
    """
    FRESH_AIR = "FreshAir"
    RETURN_AIR = "ReturnAir"
    GLYCOL = "Glycol"
    HOT_WATER = "HotWater"
    COLD_WATER = "ColdWater"
    HOT_AND_COLD_WATER = "HotAndColdWater"
    OTHER = "Other"
