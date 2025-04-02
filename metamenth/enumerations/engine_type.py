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


class EngineType(AbstractEnum):
    """
    Types of Engine

    Author: Peter Yefi
    Email: peteryefi@gmail.com
    """
    FUEL_CELL = "FuelCell"
    STIRLING = "Stirling"
    INTERNAL_COMBUSTION = "InternalCombustion"
    MICRO_TURBINE = "MicroTurbine"
    ELECTROLYSER = "Electrolyser"
    STEAM = "Steam"
    OTHER = "Other"
