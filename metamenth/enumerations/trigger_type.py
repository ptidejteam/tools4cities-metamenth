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


class TriggerType(Enum):
    """
    How different actuators can be triggered

    Author: Peter Yefi
    Email: peteryefi@gmail.com
    """
    ON = "On"
    OFF = "Off"
    OPEN = "Open"
    CLOSE = "Close"
    OPEN_CLOSE = "OpenClose"


