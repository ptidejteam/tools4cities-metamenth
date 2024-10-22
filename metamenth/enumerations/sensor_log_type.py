from metamenth.enumerations.abstract_enum import AbstractEnum


class SensorLogType(AbstractEnum):
    """
    Describes how sensor values are recorded

    Author: Peter Yefi
    Email: peteryefi@gmail.com
    """
    POLLING = "Polling"
    CHANGE_OF_VALUE = "ChangeOfValue"
