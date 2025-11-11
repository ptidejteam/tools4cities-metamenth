"""
Copyright (c) 2023-2025 Peter Yefi.
All rights reserved. This program and the accompanying materials
are made available under the terms of the GNU General Public License v3.0
which accompanies this distribution, and is available at:
https://www.gnu.org/licenses/gpl-3.0.html

Contributors:
    Peter Yefi - API design and implementation
"""

from metamenth.measure_instruments.interfaces.abstract_data_measure import AbstractDataMeasure
from metamenth.enumerations import DataMeasurementType


class MeterMeasure(AbstractDataMeasure):
    """
    This class represents the reading values of a meter in a building.
    The unit of measurement depends on the phenomenon measured by a meter

    Author: Peter Yefi
    Email: peteryefi@gmail.com
    """

    def __init__(self, value: float, timestamp: str = None, measurement_type: DataMeasurementType = None):
        """
        :param value: The numerical value measured
        :param timestamp: the time of measurement
        :param measurement_type: the type of the measurment, e.g., electricity consumption

        """
        super().__init__(value, timestamp, measurement_type)
