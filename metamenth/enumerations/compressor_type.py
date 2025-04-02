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

