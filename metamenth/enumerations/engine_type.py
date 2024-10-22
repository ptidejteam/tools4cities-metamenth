from metamenth.enumerations.abstract_enum import AbstractEnum


class EngineType(AbstractEnum):
    """
    Types of Engine

    Author: Peter Yefi
    Email: peteryefi@gmail.com
    """
    FUEL_CELL = "FuelCell"
    STIRLING = "Stirling"
    INTERNAL_COMBUSTION = "InternalCombustion"
    MICRO_TURBINE = "MicroTurbine"
    ELECTROLYSER = "Electrolyser"
    STEAM = "Steam"
    OTHER = "Other"
