"""
Copyright (c) 2023-2025 Peter Yefi.
All rights reserved. This program and the accompanying materials
are made available under the terms of the GNU General Public License v3.0
which accompanies this distribution, and is available at:
https://www.gnu.org/licenses/gpl-3.0.html

Contributors:
    Peter Yefi - API design and implementation
"""

from dataclasses import dataclass
from metamenth.enumerations import MeasurementUnit


@dataclass
class Measure:
    unit: MeasurementUnit = None
    minimum: float = 0.0
    maximum: float = 0.0
    slope: float = 0.0
    exponent: float = 0.0
    mantissa: float = 0.0
