"""
Copyright (c) 2023-2025 Peter Yefi.
All rights reserved. This program and the accompanying materials
are made available under the terms of the GNU General Public License v3.0
which accompanies this distribution, and is available at:
https://www.gnu.org/licenses/gpl-3.0.html

Contributors:
    Peter Yefi - API design and implementation
"""

from dataclasses import dataclass
from metamenth.enumerations import WaveForm
from metamenth.datatypes.interfaces.abstract_measure import AbstractMeasure


@dataclass
class RatedDeviceMeasure:
    voltage_rating: AbstractMeasure
    current_rating: AbstractMeasure
    frequency: AbstractMeasure = None
    power_factor: float = 0.0
    phase: float = 0.0
    voltage_output: AbstractMeasure = None
    current_output: AbstractMeasure = None
    power_output: AbstractMeasure = None
    waveform: WaveForm = None
    efficiency: AbstractMeasure = None
