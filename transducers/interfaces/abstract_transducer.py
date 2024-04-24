from abc import ABC
from typing import Dict, Any
from datatypes.continuous_measure import ContinuousMeasure
from uuid import uuid4
import sys
from utils import StructureEntitySearch
from typing import List
from typing import Union
from measure_instruments.sensor_data import SensorData
from measure_instruments.trigger_history import TriggerHistory
from datatypes.interfaces.abstract_measure import AbstractMeasure
from enumerations import MeasurementUnit


class AbstractTransducer(ABC):
    def __init__(self,
                 name: str,
                 registry_id: str = None,
                 input_voltage_range: ContinuousMeasure = None,
                 input_current_range: ContinuousMeasure = None,
                 output_current_range: ContinuousMeasure = None,
                 output_voltage_range: ContinuousMeasure = None):
        """
        Describes a transducers (in a building)
        :param name: the unique name of the transducers
        :param registry_id: the registry id of the transducers
        :param set_point: the set point associated with the data this sensor measures
        :param input_voltage_range: the input voltage range of the transducers
        :param input_current_range: the input current range of the transducers
        :param output_current_range: the output current range of the transducers
        :param output_voltage_range: the output voltage range of the transducers
        """
        self.UID = uuid4()
        self.name = name
        self.input_voltage_range = input_voltage_range
        self.input_current_range = input_current_range
        self.registry_id = registry_id
        self._set_point = None
        self.output_current_range = output_current_range
        self.output_voltage_range = output_voltage_range
        self.meta_data: Dict[str, Any] = {}
        self._data = []

    def set_set_point(self, value: AbstractMeasure, measure: MeasurementUnit):
        if value is not None and measure is not None:
            if value.measurement_unit != measure.unit:
                raise ValueError('(Input) sensor measure: {} not matching set point measure: {}'
                                 .format(value.measurement_unit, measure.unit))
        self._set_point = value

    def add_data(self, data: Union[List[TriggerHistory], List[SensorData]]):
        if data is None:
            raise ValueError('data should be a list of SensorData or TriggerHistory')
        self._data.extend(data)

    def remove_data(self, data: Union[TriggerHistory, SensorData]):
        self._data.remove(data)

    def add_meta_data(self, key, value):
        """
        Adds meta data to transducers
        :param key: the key part of the metadata
        :param value: the value part of the metadata
        :return:
        """
        self.meta_data[key] = value

    def remove_meta_data(self, key):
        """
        removes meta data to transducers
        :param key: the key part of the metadata
        :return:
        """
        try:
            del self.meta_data[key]
        except KeyError as err:
            print(err, file=sys.stderr)

    def get_data(self, search_terms: Dict = None) -> Union[List[SensorData], List[TriggerHistory]]:
        """
        Search data by attributes values
        :param search_terms: a dictionary of attributes and their values
        :return [SensorData|TriggerHistory]:
        """
        return StructureEntitySearch.search(self._data, search_terms)

    def get_data_by_date(self, from_timestamp: str, to_timestamp: str = None) -> Union[List[SensorData],
                                                                                       List[TriggerHistory]]:
        """
        searches transducer data based on provided timestamp
        :param from_timestamp: the start timestamp
        :param to_timestamp: the end timestamp
        :return: [SensorData|TriggerHistory]
        """
        return StructureEntitySearch.date_range_search(self._data, from_timestamp, to_timestamp)

    def __eq__(self, other):
        if isinstance(other, AbstractTransducer):
            # Check for equality based on the 'name' attribute
            return self.name == other.name
        return False

    def __str__(self):
        return (f"Unit: {self.UID}, Name: {self.name}, Registry ID: {self.registry_id}, "
                f"Set Point: {self._set_point}, "
                f"Input Voltage Range: {self.input_voltage_range}, "
                f"Output Voltage Range: {self.output_voltage_range}, "
                f"Input Current Range: {self.input_current_range}, "
                f"Output Current Range: {self.output_current_range}, "
                f"Metadata: {self.meta_data})")

