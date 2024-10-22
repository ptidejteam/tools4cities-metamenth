from metamenth.enumerations.abstract_enum import AbstractEnum


class CompressorType(AbstractEnum):
    """
    Types of compressor

    Author: Peter Yefi
    Email: peteryefi@gmail.com
    """
    RECIPROCATING_HERMETIC = "ReciprocatingHermetic"
    RECIPROCATING_SEMI_HERMETIC = "ReciprocatingSemiHermetic"
    RECIPROCATING_OPEN = "ReciprocatingOpen"
    ROTARY_VANE = "RotaryVane"
    SCROLL = "Scroll"
    SCREW = "Screw"
    CENTRIFUGAL = "Centrifugal"
    OTHER = "Other"

