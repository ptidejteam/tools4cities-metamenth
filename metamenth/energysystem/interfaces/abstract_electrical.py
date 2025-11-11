"""
Copyright (c) 2023-2025 Peter Yefi.
All rights reserved. This program and the accompanying materials
are made available under the terms of the GNU General Public License v3.0
which accompanies this distribution, and is available at:
https://www.gnu.org/licenses/gpl-3.0.html

Contributors:
    Peter Yefi - API design and implementation
"""

from metamenth.enumerations import PowerState
from metamenth.energysystem.interfaces.abstract_common_energy_system import AbstractCommonEnergySystem


class AbstractElectrical(AbstractCommonEnergySystem):

    def __init__(self,  name: str, power_state: PowerState):
        super().__init__(name)
        self._power_state = None

        self.power_state = power_state

    @property
    def power_state(self) -> PowerState:
        return self._power_state

    @power_state.setter
    def power_state(self, value: PowerState):
        if value is None:
            raise ValueError('power_state must be on type PowerState')
        self._power_state = value

    def __str__(self):
        return (
            f"{super().__str__()}"
            f"Power State: {self.power_state}, "
        )