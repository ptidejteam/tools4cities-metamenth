from metamenth.enumerations.abstract_enum import AbstractEnum


class EngineMode(AbstractEnum):
    """
    Modes of Engine

    Author: Peter Yefi
    Email: peteryefi@gmail.com
    """
    HEATING = "Heating"
    ELECTRICITY = "Electricity"
    CO_GENERATION = "CoGeneration"
    FUEL = "Fuel"
    OTHER = "Other"
