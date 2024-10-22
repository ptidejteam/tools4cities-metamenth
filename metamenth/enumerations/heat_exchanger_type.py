from metamenth.enumerations.abstract_enum import AbstractEnum


class HeatExchangerType(AbstractEnum):
    """
    Types of heat exchangers

    Author: Peter Yefi
    Email: peteryefi@gmail.com
    """
    PLATE = "Plate"
    SHELL_AND_TUBE = "ShellAndTube"
    FIN_TUBE = "FinTube"
    PLATED_FIN = "PlatedFin"
    OTHER = "Other"

