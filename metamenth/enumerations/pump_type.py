from metamenth.enumerations.abstract_enum import AbstractEnum


class PumpType(AbstractEnum):
    """
    Different types of pumps (not heat pumps)

    Author: Peter Yefi
    Email: peteryefi@gmail.com
    """
    CENTRIFUGAL = "On"
    CIRCULATOR = "Off"
    CONDENSER = "StandBy"
    BOOSTER = "OutOfService"
    CONDENSATE = "VariableSpeed"
    OTHER = "Other"

