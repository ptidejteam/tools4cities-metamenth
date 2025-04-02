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


class DuctSubType(AbstractEnum):
    """
    Subtypes of ducts

    Author: Peter Yefi
    Email: peteryefi@gmail.com
    """
    FRESH_AIR = "FreshAir"
    RETURN_AIR = "ReturnAir"
    MIXED_AIR = "MixedAir"
    GLYCOL = "Glycol"
    HOT_WATER = "HotWater"
    COLD_WATER = "ColdWater"
    HOT_AND_COLD_WATER = "HotAndColdWater"
    OTHER = "Other"
