from enumerations.abstract_enum import AbstractEnum


class EngineMode(AbstractEnum):
    """
    Modes of Engine

    Author: Peter Yefi
    Email: peteryefi@gmail.com
    """
    HEATING = "Heating"
    ELECTRICITY = "Electricity"
    COGENERATION = "CoGeneration"
    FUEL = "Fuel"
    OTHER = "Other"
