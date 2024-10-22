from metamenth.enumerations.abstract_enum import AbstractEnum


class BoilerCategory(AbstractEnum):
    """
    Types of heating

    Author: Peter Yefi
    Email: peteryefi@gmail.com
    """
    LPG = "LPG"
    NATURAL_GAS = "NaturalGas"
    OIL_FIRED = "OilFired"
    BIOMASS = "Biomass"
    WOOD_CHIPS = "WoodChips"
    ELECTRICAL = "Electrical"
    OTHER = "Other"

