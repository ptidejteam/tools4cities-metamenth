"""
Copyright (c) 2023-2025 Peter Yefi.
All rights reserved. This program and the accompanying materials
are made available under the terms of the GNU General Public License v3.0
which accompanies this distribution, and is available at:
https://www.gnu.org/licenses/gpl-3.0.html

Contributors:
    Peter Yefi - API design and implementation
"""

from metamenth.subsystem.interfaces.abstract_ventilation_component import AbstractVentilationComponent
from metamenth.enumerations import HeatingType
from metamenth.enumerations import PowerState


class BaseboardHeater(AbstractVentilationComponent):

    def __init__(self, name: str, heating_type: HeatingType, power_state: PowerState):
        super().__init__(name)
        self._heating_type = None
        self._power_state = None

        self.heating_type = heating_type
        self.power_state = power_state

    @property
    def heating_type(self) -> HeatingType:
        return self._heating_type

    @heating_type.setter
    def heating_type(self, value: HeatingType):
        if value is not None:
            self._heating_type = value
        else:
            raise ValueError("heating_type must be of type HeatingType")

    @property
    def power_state(self) -> PowerState:
        return self._power_state

    @power_state.setter
    def power_state(self, value: PowerState):
        if value is not None:
            self._power_state = value
        else:
            raise ValueError("power_state must be of type PowerState")

    def __str__(self):
        return (
            f"BaseboardHeater ({super().__str__()}"
            f"Heating Type: {self.heating_type}"
            f"Power State: {self.power_state.value})"
        )

