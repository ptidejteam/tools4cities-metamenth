from metamenth.enumerations.abstract_enum import AbstractEnum


class MeterAccumulationFrequency(AbstractEnum):
    """
    Data accumulation frequency of meters

    Author: Peter Yefi
    Email: peteryefi@gmail.com
    """
    DAILY = "Daily"
    WEEKLY = "Weekly"
    MONTHLY = "Monthly"
    QUARTERLY = "Quarterly"
    YEARLY = "Yearly"
    NONE = None

