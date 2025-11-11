"""
Copyright (c) 2023-2025 Peter Yefi.
All rights reserved. This program and the accompanying materials
are made available under the terms of the GNU General Public License v3.0
which accompanies this distribution, and is available at:
https://www.gnu.org/licenses/gpl-3.0.html

Contributors:
    Peter Yefi - API design and implementation
"""

from metamenth.energysystem.storage_system.mobile_storage_energy_system import MobileStorageEnergySystem
from metamenth.enumerations import MeasurementUnit
from metamenth.datatypes.binary_measure import BinaryMeasure
from metamenth.enumerations import V2GMode


class ElectricVehicle(MobileStorageEnergySystem):

    def __init__(self, name: str, inverter: bool, unit: MeasurementUnit, v2g_capability: bool = False):
        super().__init__(name, inverter, unit)
        self._v2g_capability = v2g_capability
        self._v2g_power_limit = None
        self._v2g_mode = None

    @property
    def v2g_capability(self) -> bool:
        return self._v2g_capability

    @v2g_capability.setter
    def v2g_capability(self, value: bool):
        self._v2g_capability = value

    @property
    def v2g_power_limit(self) -> BinaryMeasure:
        return self._v2g_power_limit

    @v2g_power_limit.setter
    def v2g_power_limit(self, value: BinaryMeasure):
        self._v2g_power_limit = value

    @property
    def v2g_mode(self) -> V2GMode:
        return self._v2g_mode

    @v2g_mode.setter
    def v2g_mode(self, value: V2GMode):
        self._v2g_mode = value

    def __str__(self):
        return (
            f"ElectricVehicle("
            f"{super().__str__()} "
            f"V2G Capability: {self.v2g_capability}, "
            f"V2G Power Limit: {self.v2g_power_limit}, "
            f"V2G Mode: {self.v2g_mode})"
        )