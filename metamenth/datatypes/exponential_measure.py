"""
Copyright (c) 2023-2025 Peter Yefi.
All rights reserved. This program and the accompanying materials
are made available under the terms of the GNU General Public License v3.0
which accompanies this distribution, and is available at:
https://www.gnu.org/licenses/gpl-3.0.html

Contributors:
    Peter Yefi - API design and implementation
"""

from metamenth.datatypes.interfaces.abstract_range_measure import AbstractRangeMeasure
from metamenth.datatypes.measure import Measure


class ExponentialMeasure(AbstractRangeMeasure):
    """
    Exponential measurement

    Author: Peter Yefi
    Email: peteryefi@gmail.com
    """
    def __init__(self, measure: Measure):
        super().__init__(measure)
        self.exponent = measure.exponent
        self.mantissa: measure.mantissa

    def __str__(self):
        return (
            f"ExponentialMeasure("
            f"Exponent: {self.exponent}, "
            f"Mantissa: {self.maximum}, "
            f"{super().__str__()})"
        )