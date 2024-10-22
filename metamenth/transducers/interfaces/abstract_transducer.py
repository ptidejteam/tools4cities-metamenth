from abc import ABC
from typing import Dict, Any
from metamenth.datatypes.continuous_measure import ContinuousMeasure
from uuid import uuid4
import sys
from metamenth.utils import StructureEntitySearch
from typing import List
from typing import Union
from metamenth.measure_instruments.sensor_data import SensorData
from metamenth.measure_instruments.trigger_history import TriggerHistory


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
        self.output_current_range = output_current_range
        self.output_voltage_range = output_voltage_range
        self.meta_data: Dict[str, Any] = {}
        self._data = []

    def add_data(self, data: Union[List[TriggerHistory], List[SensorData]]):
        if data is None:
            raise ValueError('data should be a list of SensorData or TriggerHistory')
        self._data.extend(data)

    def remove_data(self, data: Union[TriggerHistory, SensorData]):
        self._data.remove(data)

    def add_meta_data(self, key, value):
        """
        Adds metadata to transducers
        :param key: the key part of the metadata
        :param value: the value part of the metadata
        :return:
        """
        self.meta_data[key] = value

    def remove_meta_data(self, key):
        """
        removes metadata to transducers
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

    def get(self, attribute):
        return getattr(self, attribute, None)

    def __eq__(self, other):
        if isinstance(other, AbstractTransducer):
            # Check for equality based on the 'name' attribute
            return self.name == other.name
        return False

    def __str__(self):
        return (f"Unit: {self.UID}, Name: {self.name}, Registry ID: {self.registry_id}, "
                f"Input Voltage Range: {self.input_voltage_range}, "
                f"Output Voltage Range: {self.output_voltage_range}, "
                f"Input Current Range: {self.input_current_range}, "
                f"Output Current Range: {self.output_current_range}, "
                f"Metadata: {self.meta_data})")

