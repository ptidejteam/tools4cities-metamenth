from metamenth.enumerations.abstract_enum import AbstractEnum


class SolarDistributionType(AbstractEnum):
    """
    Solar distribution of buildings

    Author: Peter Yefi
    Email: peteryefi@gmail.com
    """
    FULL_EXTERIOR = "FullExterior"
    MINIMAL_SHADOWING = "MinimalShadowing"
    FULL_INTERIOR_AND_EXTERIOR = "FullInteriorAndExterior"
    FULL_EXTERIOR_WITH_REFLECTIONS = "FullExteriorWithReflections"
    FULL_INTERIOR_AND_EXTERIOR_WITH_REFLECTIONS = "FullInteriorAndExteriorWithReflections"
