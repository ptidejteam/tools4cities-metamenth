"""
Copyright (c) 2023-2025 Peter Yefi.
All rights reserved. This program and the accompanying materials
are made available under the terms of the GNU General Public License v3.0
which accompanies this distribution, and is available at:
https://www.gnu.org/licenses/gpl-3.0.html

Contributors:
    Peter Yefi - API design and implementation
"""

from enum import Enum
from fuzzywuzzy import fuzz


class AbstractEnum(Enum):

    @classmethod
    def get_enum_type(cls, value: str):
        try:
            value = value.replace(" ", "_").replace("-", "_").upper()
            closest_key = max(cls.__members__.keys(), key=lambda k: fuzz.ratio(value.lower(), k.lower()))
            return cls[closest_key]
        except KeyError:
            return None
