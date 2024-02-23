from enum import Enum


class SensorLogType(Enum):
    """
    Describes how sensor values are recorded

    Author: Peter Yefi
    Email: peteryefi@gmail.com
    """
    POLLING = "Polling"
    CHANGE_OF_VALUE = "ChangeOfValue"
