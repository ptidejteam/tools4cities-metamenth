"""
Copyright (c) 2023-2025 Peter Yefi.
All rights reserved. This program and the accompanying materials
are made available under the terms of the GNU General Public License v3.0
which accompanies this distribution, and is available at:
https://www.gnu.org/licenses/gpl-3.0.html

Contributors:
    Peter Yefi - API design and implementation
"""

from metamenth.enumerations import TriggerType
from metamenth.measure_instruments.interfaces.abstract_data_measure import AbstractDataMeasure


class TriggerHistory(AbstractDataMeasure):

    def __init__(self, trigger_type: TriggerType, value: float = None, timestamp: str = None):
        if value is None:
            value = 0.0
        super().__init__(value, timestamp)
        self.trigger_type = trigger_type

    def __eq__(self, other):
        if isinstance(other, TriggerHistory):
            return self.UID == other.UID
        return False
