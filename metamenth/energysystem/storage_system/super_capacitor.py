"""
Copyright (c) 2023-2025 Peter Yefi.
All rights reserved. This program and the accompanying materials
are made available under the terms of the GNU General Public License v3.0
which accompanies this distribution, and is available at:
https://www.gnu.org/licenses/gpl-3.0.html

Contributors:
    Peter Yefi - API design and implementation
"""

from metamenth.energysystem.storage_system.immobile_storage_energy_system import ImmobileStorageEnergySystem
from metamenth.enumerations import MeasurementUnit
from metamenth.enumerations import EnergySource
from metamenth.enumerations import CapacitorTech


class SuperCapacitor(ImmobileStorageEnergySystem):
    def __init__(self, name: str, inverter: bool, unit: MeasurementUnit,
                 energy_source: EnergySource, tech: CapacitorTech):
        super().__init__(name, inverter, unit, energy_source, tech)

    def __str__(self):
        return (
            f"SuperCapacitor("
            f"{super().__str__()})"
        )
