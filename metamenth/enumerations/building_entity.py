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


class BuildingEntity(Enum):
    """
    Various building Entity

    Author: Peter Yefi
    Email: peteryefi@gmail.com
    """
    BUILDING = "Building"
    FLOOR = "Floor"
    SCHEDULE = "Schedule"
    METER = "Meter"
    WEATHER_STATION = "WeatherStation"
    ROOM = "Room"
    OPEN_SPACE = "OpenSpace"
    TRANSDUCER = "Transducer"
    SPACE = "Space"
    ADJACENT_ZONE = "AdjacentZone"
    OVERLAPPING_ZONE = "OverlappingZone"
    ZONE = "Zone"
    ADJACENT_SPACE = "AdjacentSpace"
    SUBSYSTEM = "Subsystem"
    APPLIANCE = "Appliance"
    HVAC_COMPONENT = "HVACComponent"
    FLOOR_SPACE = "FloorSpace"
    ENERGY_SYSTEM = "EnergySystem"


