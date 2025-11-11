"""
Copyright (c) 2023-2025 Peter Yefi.
All rights reserved. This program and the accompanying materials
are made available under the terms of the GNU General Public License v3.0
which accompanies this distribution, and is available at:
https://www.gnu.org/licenses/gpl-3.0.html

Contributors:
    Peter Yefi - API design and implementation
"""

from datetime import datetime
from dataclasses import dataclass
from typing import Type
from metamenth.datatypes.interfaces.abstract_measure import AbstractMeasure
from uuid import uuid4


@dataclass
class OperationalSchedule:
    UID = uuid4()
    name: str # unique name for operational schedule
    start_date: datetime
    end_date: datetime
    setPoint: Type[AbstractMeasure] = None
    recurring: bool = True

    def __eq__(self, other):
        # schedules are equal if they share the same name
        if isinstance(other, OperationalSchedule):
            # Check for equality based on the 'name' attribute
            return self.name == other.name
        return False
