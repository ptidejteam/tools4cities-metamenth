from enumerations.abstract_enum import AbstractEnum


class PowerState(AbstractEnum):
    """
    Power states of an HVAC component

    Author: Peter Yefi
    Email: peteryefi@gmail.com
    """
    ON = "On"
    OFF = "Off"
    OUT_OF_SERVICE = "OutOfService"
    OTHER = "Other"

