from metamenth.enumerations.abstract_enum import AbstractEnum


class PowerState(AbstractEnum):
    """
    Power states of an HVAC component

    Author: Peter Yefi
    Email: peteryefi@gmail.com
    """
    ON = "On"
    OFF = "Off"
    STANDBY = "StandBy"
    OUT_OF_SERVICE = "OutOfService"
    VARIABLE_SPEED = "VariableSpeed"
    INTERMITTENT = "Intermittent"
    BOOST = "Boost"
    NIGHT_MODE = "NightMode"
    NONE = "None"
    OTHER = "Other"

