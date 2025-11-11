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


class PowerState(AbstractEnum):
    """
    Power states of an HVAC component

    Author: Peter Yefi
    Email: peteryefi@gmail.com
    """
    ON = "On"
    OFF = "Off"
    STANDBY = "StandBy"
    OUT_OF_SERVICE = "OutOfService"
    VARIABLE_SPEED = "VariableSpeed"
    INTERMITTENT = "Intermittent"
    BOOST = "Boost"
    NIGHT_MODE = "NightMode"
    NONE = "None"
    OTHER = "Other"

