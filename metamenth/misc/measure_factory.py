"""
Copyright (c) 2023-2025 Peter Yefi.
All rights reserved. This program and the accompanying materials
are made available under the terms of the GNU General Public License v3.0
which accompanies this distribution, and is available at:
https://www.gnu.org/licenses/gpl-3.0.html

Contributors:
    Peter Yefi - API design and implementation
"""

from metamenth.datatypes.binary_measure import BinaryMeasure
from metamenth.datatypes.linear_measure import LinearMeasure
from metamenth.datatypes.continuous_measure import ContinuousMeasure
from metamenth.datatypes.exponential_measure import ExponentialMeasure
from metamenth.datatypes.interfaces.abstract_measure import AbstractMeasure
from metamenth.datatypes.measure import Measure


class MeasureFactory:
    """
    A factory class that returns various types of measures
    """
    @staticmethod
    def create_measure(measure_type: str, measure: Measure) -> AbstractMeasure:
        if measure_type == "Binary":
            return BinaryMeasure(measure)
        elif measure_type == "Linear":
            return LinearMeasure(measure)
        elif measure_type == "Continuous":
            return ContinuousMeasure(measure)
        elif measure_type == "Exponential":
            return ExponentialMeasure(measure)
        else:
            raise ValueError("Invalid measure type")
