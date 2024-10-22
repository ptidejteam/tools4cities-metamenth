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
