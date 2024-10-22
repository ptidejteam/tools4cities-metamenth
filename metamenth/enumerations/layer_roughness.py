from metamenth.enumerations.abstract_enum import AbstractEnum


class LayerRoughness(AbstractEnum):
    """
    Different types of material roughness

    Author: Peter Yefi
    Email: peteryefi@gmail.com
    """

    VERY_ROUGH = "VeryRough (0.04m)"
    ROUGH = "Rough (0.01m)"
    MEDIUM_ROUGH = "MediumRough (0.005m)"
    SMOOTH = "Smooth (0.0005m)"
    VERY_SMOOTH = "VerySmooth (0.0001m)"

