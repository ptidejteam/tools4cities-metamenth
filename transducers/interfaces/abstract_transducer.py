from abc import ABC, abstractmethod
from typing import Dict, Any
from datatypes.continuous_measure import ContinuousMeasure
from uuid import uuid4


class AbstractTransducer(ABC):
    def __init__(self,
                 name: str,
                 registry_id: str = None,
                 input_voltage_range: ContinuousMeasure = None,
                 input_current_range: ContinuousMeasure = None,
                 output_current_range: ContinuousMeasure = None,
                 output_voltage_range: ContinuousMeasure = None,
                 change_of_value: bool = False):
        """
        Describes a transducers (in a building)
        :param name: the unique name of the transducers
        :param registry_id: the registry id of the transducers
        :param input_voltage_range: the input voltage range of the transducers
        :param input_current_range: the input current range of the transducers
        :param output_current_range: the output current range of the transducers
        :param output_voltage_range: the output voltage range of the transducers
        :param change_of_value: indicates if data is recorded based on change of value (COV)
        """
        self.UID = uuid4()
        self.name = name
        self.input_voltage_range = input_voltage_range
        self.input_current_range = input_current_range
        self.registry_id = registry_id
        self.output_current_range = output_current_range
        self.output_voltage_range = output_voltage_range
        self.change_of_value = change_of_value
        self.meta_data: Dict[str, Any] = {}
        self._data = []

    @abstractmethod
    def add_data(self, data):
        pass

    @abstractmethod
    def remove_data(self, data):
        pass

    def add_meta_data(self, key, value):
        """
        Adds meta data to transducers
        :param key: the key part of the metadata
        :param value: the value part of the metadata
        :return:
        """
        self.meta_data[key] = value

    def __str__(self):
        return (f"Unit: {self.UID}, Name: {self.name}, Registry ID: {self.registry_id}, "
                f"Input Voltage Range: {self.input_voltage_range}, "
                f"Output Voltage Range: {self.output_voltage_range}, "
                f"Input Current Range: {self.input_current_range}, "
                f"Output Current Range: {self.output_current_range}, "
                f"Change of Value: {self.change_of_value}, "
                f"Metadata: {self.meta_data})")

