from enumerations.abstract_enum import AbstractEnum


class EngineSubType(AbstractEnum):
    """
    Modes of Engine

    Author: Peter Yefi
    Email: peteryefi@gmail.com
    """
    DIESEL = "Diesel"
    NATURAL_GAS = "NaturalGas"
    HYDROGEN = "Hydrogen"
    PETROL = "Petrol"
    COAL = "Coal"
    OTHER = "Other"
