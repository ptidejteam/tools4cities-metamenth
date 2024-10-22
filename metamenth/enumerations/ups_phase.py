from metamenth.enumerations.abstract_enum import AbstractEnum


class UPSPhase(AbstractEnum):
    """
    Different phases of uninterruptible power supply

    Author: Peter Yefi
    Email: peteryefi@gmail.com
    """
    SINGLE = "Single"
    THREE = "Three"
    SPLIT = "Split"
