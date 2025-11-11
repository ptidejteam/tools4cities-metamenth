"""
Copyright (c) 2023-2025 Peter Yefi.
All rights reserved. This program and the accompanying materials
are made available under the terms of the GNU General Public License v3.0
which accompanies this distribution, and is available at:
https://www.gnu.org/licenses/gpl-3.0.html

Contributors:
    Peter Yefi - API design and implementation
"""

from metamenth.enumerations.abstract_enum import AbstractEnum


class V2GMode(AbstractEnum):
    """
    Vehicle to grid mode of electric vehicle

    Author: Peter Yefi
    Email: peteryefi@gmail.com
    """
    FREQUENCY_REGULATION = "FrequencyRegulation"
    PEAK_SHAVING = "PeakShaving"
    ENERGY_ARBITRAGE = "EnergyArbitrage"
    OTHER = "Other"
