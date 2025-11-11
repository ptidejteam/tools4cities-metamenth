"""
Copyright (c) 2023-2025 Peter Yefi.
All rights reserved. This program and the accompanying materials
are made available under the terms of the GNU General Public License v3.0
which accompanies this distribution, and is available at:
https://www.gnu.org/licenses/gpl-3.0.html

Contributors:
    Peter Yefi - API design and implementation
"""

from metamenth.energysystem.interfaces.abstract_electrical import AbstractElectrical
from metamenth.enumerations import PowerState
from metamenth.datatypes.binary_measure import BinaryMeasure


class Alternator(AbstractElectrical):
    def __init__(self, name: str, power_state: PowerState = PowerState.NONE):
        super().__init__(name, power_state)

        self._power_rating = None

    @property
    def power_rating(self) -> BinaryMeasure:
        return self._power_rating

    @power_rating.setter
    def power_rating(self, value: BinaryMeasure):
        self._power_rating = value

    def __str__(self):
        return (
            f"Alternator("
            f"{super().__str__()}"
            f"Power Rating: {self.power_rating})"
        )

