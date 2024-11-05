from metamenth.enumerations.abstract_enum import AbstractEnum


class AnemometerType(AbstractEnum):
    """
    Types of anemometers

    Author: Peter Yefi
    Email: peteryefi@gmail.com
    """
    VANE = "Vane"
    HOT_WIRE = "HotWire"
    PITOT_TUBE = "PitotTube"

