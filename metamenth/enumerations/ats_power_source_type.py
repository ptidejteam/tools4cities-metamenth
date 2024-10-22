from metamenth.enumerations.abstract_enum import AbstractEnum


class ATSPowerSourceType(AbstractEnum):
    """
    Type of ATS power sources

    Author: Peter Yefi
    Email: peteryefi@gmail.com
    """
    UTILITY_GENERATOR = "UtilityGenerator"
    UTILITY_UTILITY = "UtilityUtility"
    GENERATOR_GENERATOR = "GeneratorGenerator"
    UTILITY_UTILITY_GENERATOR = "UtilityUtilityGenerator"
    UTILITY_GENERATOR_GENERATOR = "UtilityGeneratorGenerator"
    OTHER = "Other"
