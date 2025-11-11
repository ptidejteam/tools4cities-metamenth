"""
Copyright (c) 2023-2025 Peter Yefi.
All rights reserved. This program and the accompanying materials
are made available under the terms of the GNU General Public License v3.0
which accompanies this distribution, and is available at:
https://www.gnu.org/licenses/gpl-3.0.html

Contributors:
    Peter Yefi - API design and implementation
"""

from metamenth.subsystem.interfaces.abstract_subsystem import AbstractSubsystem
from metamenth.subsystem.hvac_system import HVACSystem


class BuildingControlSystem(AbstractSubsystem):

    def __init__(self, name: str):
        super().__init__(name)
        self._hvac_system = None

    @property
    def hvac_system(self) -> HVACSystem:
        return self._hvac_system

    @hvac_system.setter
    def hvac_system(self, value: HVACSystem):
        if value is not None:
            self._hvac_system = value
        else:
            raise ValueError("hvac_system must be of type HVACSystem")

    def __str__(self):
        return (
            f"BuildingControlSystem ({super().__str__()}"
            f"HVAC System: {self.hvac_system}"
        )

