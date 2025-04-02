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


class SensorMeasureType(Enum):
    """
    Various sensor measurement types

    Author: Peter Yefi
    Email: peteryefi@gmail.com
    """
    THERMO_COUPLE_TYPE_A = "ThermoCoupleTypeA"
    THERMO_COUPLE_TYPE_B = "ThermoCoupleTypeB"
    THERMO_COUPLE_TYPE_C = "ThermoCoupleTypeC"
    THERMO_COUPLE_TYPE_D = "ThermoCoupleTypeD"
    THERMO_COUPLE_TYPE_E = "ThermoCoupleTypeE"
    THERMO_COUPLE_TYPE_F = "ThermoCoupleTypeF"
    PT_100 = "PT100"
    PIEZO_RESISTIVE_PRESSURE = "PiezoResistivePressure"
    ANALOGUE_PRESSURE = "AnaloguePressure"
    PASSIVE_INFRARED = "PassiveInfrared"
