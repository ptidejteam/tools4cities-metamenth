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


class StatusMeasure(AbstractDataMeasure):

    def __init__(self, status: str, timestamp: str = None):
        """
        :param status: The string value measured
        :param timestamp: the time of measurement
        """
        super().__init__(status, timestamp)

