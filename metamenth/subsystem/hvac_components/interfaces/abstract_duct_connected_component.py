"""
Copyright (c) 2023-2025 Peter Yefi.
All rights reserved. This program and the accompanying materials
are made available under the terms of the GNU General Public License v3.0
which accompanies this distribution, and is available at:
https://www.gnu.org/licenses/gpl-3.0.html

Contributors:
    Peter Yefi - API design and implementation
"""

from metamenth.subsystem.hvac_components.interfaces.abstract_hvac_component import AbstractHVACComponent
from metamenth.subsystem.hvac_components.variable_frequency_drive import VariableFrequencyDrive


class AbstractDuctConnectedComponent(AbstractHVACComponent):

    def __init__(self, name: str):
        super().__init__(name)

        self._ducts: [] = []
        self._vfd = None

    @property
    def ducts(self) -> []:
        return self._ducts.copy()

    @property
    def vfd(self) -> VariableFrequencyDrive:
        return self._vfd

    def add_duct(self, duct):
        from metamenth.subsystem.hvac_components.duct import Duct
        if duct is not None and isinstance(duct, Duct):
            self._ducts.append(duct)
        else:
            raise ValueError("value provided is not a duct")

    @vfd.setter
    def vfd(self, value: VariableFrequencyDrive):
        self._vfd = value

    def __str__(self):
        return (
            f"({super().__str__()}"
            f"Ducts {self.ducts}, "
            f"VFD: {self.vfd}, "
        )