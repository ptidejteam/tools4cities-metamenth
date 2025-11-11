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


class OpenSpaceType(AbstractEnum):
    """
    Open spaces on floors of buildings

    Author: Peter Yefi
    Email: peteryefi@gmail.com
    """
    PARKING_GARAGE = "Parking Garage"
    POOL_AREA = "Pool Area"
    OPEN_OFFICE = "Open Office"
    HALL = "Hall"
    CORRIDOR = "Corridor"
    STAIR_AREA = "StairArea"
    DINNING_AREA = "DinningArea"
    ESCALATOR_AREA = "EscalatorArea"
    RECEPTION_AREA = "ReceptionArea"
    TODDLERS_AREA = "ToddlersArea"
    OPEN_AREA = "OpenArea"
    SITTING_AREA = "SittingArea"
    OTHER = "Other"
