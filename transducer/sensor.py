from abc import ABC
from .abstract_transducer import AbstractTransducer
from typing import Optional
from enumerations import SensorMeasure
from enumerations import MeasurementUnit
from enumerations import MeasureType
from measure_instruments import SensorData
from typing import List


class Sensor(AbstractTransducer, ABC):

    def __init__(self, name: str,  measure: SensorMeasure, unit: MeasurementUnit, measure_type: MeasureType,
                 data_frequency: int, currentValue: Optional[float] = None):
        """
        :param name: the unique name of a sensor
        :param measure: the phenomenom (e.g., temperature) this sensor measures
        :param unit: the measurement unit of the data being measured
        :param measure_type: the type of data measured by the sensor
        :param data_frequency: what interval is the data recorded
        :param currentValue: the current value for the sensor
        """
        super().__init__(name)
        self.measure = measure
        self.data_frequency = data_frequency
        self.unit = unit
        self.currentValue = currentValue
        self.measure_type = measure_type
        self.data: [SensorData] = []

    def add_data(self, data: List[SensorData]):
        """
        Adds data to a sensor
        :param data: the sensor data to be added
        :return:
        """
        self.data.extend(data)

    def __str__(self):
        sensor_data = "\n".join(str(data) for data in self.data)
        return (
            f"Sensor("
            f"{super().__str__()}, "
            f"UID: {self.UID}, "
            f"Name: {self.name}, "
            f"Measure: {self.measure}, "
            f"Data Frequency: {self.data_frequency}, "
            f"Unit: {self.unit}, "
            f"CurrentValue: {self.currentValue}, "
            f"Measure Type: {self.measure_type}\n"
            f"Data Count: {len(sensor_data)}\n"
            f"Data: {sensor_data})"
        )