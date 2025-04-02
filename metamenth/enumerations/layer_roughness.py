"""
Copyright (c) 2023-2025 Peter Yefi.
All rights reserved. This program and the accompanying materials
are made available under the terms of the GNU General Public License v3.0
which accompanies this distribution, and is available at:
https://www.gnu.org/licenses/gpl-3.0.html

Contributors:
    Peter Yefi - API design and implementation
"""

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

