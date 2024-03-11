from dataclasses import dataclass
from enumerations import WaveForm
from datatypes.binary_measure import BinaryMeasure


@dataclass
class RatedDeviceMeasure:
    voltage_rating: BinaryMeasure
    current_rating: BinaryMeasure
    frequency: BinaryMeasure = None
    power_factor: float = 0.0
    phase: float = 0.0
    voltage_output: BinaryMeasure = None
    current_output: BinaryMeasure = None
    power_output: BinaryMeasure = None
    waveform: WaveForm = None
    efficiency: BinaryMeasure = None
