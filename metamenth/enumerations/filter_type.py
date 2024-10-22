from metamenth.enumerations.abstract_enum import AbstractEnum


class FilterType(AbstractEnum):
    """
    Different types of HVAC filters

    Author: Peter Yefi
    Email: peteryefi@gmail.com
    """

    FIBREGLASS = "FibreGlass"
    PLEATED = "Pleated"
    HIGH_EFFICIENCY_PARTICULAR_AIR = "HighEfficiencyParticularAir"
    ELECTROSTATIC = "Electrostatic"
    CARBON = "Carbon"
    ULTRAVIOLET_GERMICIDAL_IRRADIATION = "UltravioletGermicidalIrradiation"
    MEDIA = "Media"
    OTHER = "Other"

