"""
Copyright (c) 2023-2025 Peter Yefi.
All rights reserved. This program and the accompanying materials
are made available under the terms of the GNU General Public License v3.0
which accompanies this distribution, and is available at:
https://www.gnu.org/licenses/gpl-3.0.html

Contributors:
    Peter Yefi - API design and implementation
"""

from metamenth.datatypes.interfaces.abstract_measure import AbstractMeasure
from metamenth.datatypes.measure import Measure
from metamenth.enumerations import DataMeasurementType


class BinaryMeasure(AbstractMeasure):
    """
    Represents a binary measure with a value and a measurement unit.

    Author: Peter Yefi
    Email: peteryefi@gmail.com
    """
    def __init__(self, measure: Measure, weather_type: DataMeasurementType = None):
        super().__init__(measure, weather_type)
        self.value = measure.minimum

    def __str__(self):
        return (
            f"BinaryMeasure("
            f"Value: {self.value}, "
            f"{super().__str__()})"
        )
