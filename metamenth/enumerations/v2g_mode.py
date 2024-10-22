from metamenth.enumerations.abstract_enum import AbstractEnum


class V2GMode(AbstractEnum):
    """
    Vehicle to grid mode of electric vehicle

    Author: Peter Yefi
    Email: peteryefi@gmail.com
    """
    FREQUENCY_REGULATION = "FrequencyRegulation"
    PEAK_SHAVING = "PeakShaving"
    ENERGY_ARBITRAGE = "EnergyArbitrage"
    OTHER = "Other"
