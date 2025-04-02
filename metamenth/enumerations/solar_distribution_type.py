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


class SolarDistributionType(AbstractEnum):
    """
    Solar distribution of buildings

    Author: Peter Yefi
    Email: peteryefi@gmail.com
    """
    FULL_EXTERIOR = "FullExterior"
    MINIMAL_SHADOWING = "MinimalShadowing"
    FULL_INTERIOR_AND_EXTERIOR = "FullInteriorAndExterior"
    FULL_EXTERIOR_WITH_REFLECTIONS = "FullExteriorWithReflections"
    FULL_INTERIOR_AND_EXTERIOR_WITH_REFLECTIONS = "FullInteriorAndExteriorWithReflections"
