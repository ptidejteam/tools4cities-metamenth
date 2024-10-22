from metamenth.enumerations.abstract_enum import AbstractEnum


class CellType(AbstractEnum):
    """
    Types of cells

    Author: Peter Yefi
    Email: peteryefi@gmail.com
    """
    MONOCRYSTALLINE = "MonoCrystalline"
    POLYCRYSTALLINE = "PolyCrystalline"
    AMORPHOUS = "Amorphous"
    OTHER = "Other"
