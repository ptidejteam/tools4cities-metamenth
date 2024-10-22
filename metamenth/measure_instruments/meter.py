from metamenth.enumerations import MeterType
from metamenth.enumerations import MeasurementUnit
from metamenth.enumerations import MeterMeasureMode
from metamenth.measure_instruments.meter_measure import MeterMeasure
from metamenth.enumerations import MeterAccumulationFrequency
from typing import Dict
from metamenth.utils import StructureEntitySearch
from metamenth.measure_instruments.interfaces.abstract_reader import AbstractReader


class Meter(AbstractReader):
    """
    A representation of a meter

    Author: Peter Yefi
    Email: peteryefi@gmail.com
    """

    def __init__(self, meter_location: str, measurement_frequency: float, measurement_unit: MeasurementUnit,
                 meter_type: MeterType, measure_mode: MeterMeasureMode, data_accumulated: bool = False,
                 accumulation_frequency: MeterAccumulationFrequency = MeterAccumulationFrequency.NONE,
                 manufacturer: str = None):
        """
        Initializes a Meter instance.

        :param meter_location: The what3word location of the meter.
        :param manufacturer: The manufacturer of the meter.
        :param measurement_frequency: The measurement frequency of the meter.
        :param measurement_unit: The measurement unit of the meter data.
        :param meter_type: The type of the meter.
        :param measure_mode: the data measure mode: manual or automatic
        :param data_accumulated: indicate whether the data is accumulate or not
        :param accumulation_frequency: the frequency at which data is accumulated
        """
        super().__init__(measurement_unit, meter_location, manufacturer)
        self._measurement_frequency = None
        self._meter_type = None
        self._meter_measures: [MeterMeasure] = []
        self._measure_mode = None
        self._data_accumulated = data_accumulated
        self._accumulation_frequency = MeterAccumulationFrequency.NONE

        # Apply validation
        self.measurement_frequency = measurement_frequency
        self.meter_type = meter_type
        self.measure_mode = measure_mode
        self.accumulation_frequency = accumulation_frequency

    @property
    def measurement_frequency(self) -> float:
        return self._measurement_frequency

    @measurement_frequency.setter
    def measurement_frequency(self, value: float):
        if value is not None:
            self._measurement_frequency = value
        else:
            raise ValueError("measurement_frequency must be a float")

    @property
    def measure_mode(self) -> MeterMeasureMode:
        return self._measure_mode

    @measure_mode.setter
    def measure_mode(self, value: MeterMeasureMode):
        if value is not None:
            self._measure_mode = value
        else:
            raise ValueError("measure_mode must be a float")

    @property
    def data_accumulated(self) -> bool:
        return self._data_accumulated

    @data_accumulated.setter
    def data_accumulated(self, value: bool):
        if value is not None:
            self._data_accumulated = value
        else:
            raise ValueError("data_accumulated must be a boolean")

    @property
    def accumulation_frequency(self) -> MeterAccumulationFrequency:
        return self._accumulation_frequency

    @accumulation_frequency.setter
    def accumulation_frequency(self, value: MeterAccumulationFrequency):
        if value is not None:
            if self.data_accumulated and value is None:
                raise ValueError("accumulation_frequency must not be None")
            else:
                self._accumulation_frequency = value
        else:
            raise ValueError("data_accumulated must be a boolean")

    @property
    def meter_type(self) -> MeterType:
        return self._meter_type

    @meter_type.setter
    def meter_type(self, value: MeterType):
        if value is not None:
            self._meter_type = value
        else:
            raise ValueError("Meter type must be of type MeterType")

    def get_meter_measures(self, search_terms: Dict = None) -> [MeterMeasure]:
        """
        Search meter recordings by attributes values
        :param search_terms: a dictionary of attributes and their values
        :return [MeterMeasure]:
        """
        return StructureEntitySearch.search(self._meter_measures, search_terms)

    def get_meter_measure_by_date(self, from_timestamp: str, to_timestamp: str = None) -> [MeterMeasure]:
        """
        searches meter recordings based on provided timestamp
        :param from_timestamp: the start timestamp
        :param to_timestamp: the end timestamp
        :return: [MeterMeasure]
        """
        return StructureEntitySearch.date_range_search(self._meter_measures, from_timestamp, to_timestamp)

    def add_meter_measure(self, meter_measure: MeterMeasure):
        """
        Add measurement for this meter
        :param meter_measure: the recorded measurement by the meter.
        """
        self._meter_measures.append(meter_measure)

    def __str__(self):
        """
        :return: A formatted string representing the meter.
        """
        measurements = "\n".join(str(measure) for measure in self.get_meter_measures())

        return (
            f"Meter("
            f"{super().__str__()} "
            f"Frequency: {self.measurement_frequency}, "
            f"Measure Mode: {self.measure_mode.value}, "
            f"Data Accumulated: {self.data_accumulated}, "
            f"Accumulation Frequency: {self.accumulation_frequency.value}, "
            f"Type: {self.meter_type.value}, "
            f"Measurements: {measurements})"
        )
