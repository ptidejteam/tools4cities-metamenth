"""
Copyright (c) 2023-2025 Peter Yefi.
All rights reserved. This program and the accompanying materials
are made available under the terms of the GNU General Public License v3.0
which accompanies this distribution, and is available at:
https://www.gnu.org/licenses/gpl-3.0.html

Contributors:
    Peter Yefi - API design and implementation
"""

from uuid import uuid4
from typing import List
from metamenth.subsystem.ventilation_system import VentilationSystem


class HVACSystem:

    def __init__(self):
        self._UID = str(uuid4())
        self._ventilation_systems: List[VentilationSystem] = []

    @property
    def UID(self) -> str:
        return self._UID

    @property
    def ventilation_systems(self) -> [VentilationSystem]:
        return self._ventilation_systems.copy() if self._ventilation_systems else []

    def add_ventilation_system(self, ventilation_system:  VentilationSystem):
        if ventilation_system is not None:
            self._ventilation_systems.append(ventilation_system)
        else:
            raise ValueError("ventilation_system should be of type VentilationSystem")

    def __str__(self):
        return (
            f"HVACSystem("
            f"UID: {self.UID}, "
            f"Type: {self.ventilation_systems})"
        )