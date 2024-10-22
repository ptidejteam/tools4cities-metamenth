from enum import Enum


class TriggerType(Enum):
    """
    How different actuators can be triggered

    Author: Peter Yefi
    Email: peteryefi@gmail.com
    """
    ON = "On"
    OFF = "Off"
    OPEN = "Open"
    CLOSE = "Close"
    OPEN_CLOSE = "OpenClose"


