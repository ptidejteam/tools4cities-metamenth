"""
Copyright (c) 2023-2025 Peter Yefi.
All rights reserved. This program and the accompanying materials
are made available under the terms of the GNU General Public License v3.0
which accompanies this distribution, and is available at:
https://www.gnu.org/licenses/gpl-3.0.html

Contributors:
    Peter Yefi - API design and implementation
"""

from abc import ABC
from metamenth.datatypes.measure import Measure
from metamenth.enumerations import DataMeasurementType


class AbstractMeasure(ABC):
    """
    Defines properties shared by all measures

    Author: Peter Yefi
    Email: peteryefi@gmail.com
    """
    def __init__(self, measure: Measure, measure_type: DataMeasurementType = None):
        self.measurement_unit = measure.unit
        self.measure_type = measure_type

    def __str__(self):
        return f"Unit: {self.measurement_unit.value}, " \
               f"Measure Type: {self.measure_type.value if self.measure_type is not None else self.measure_type}"
