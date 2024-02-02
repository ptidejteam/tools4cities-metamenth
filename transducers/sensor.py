from abc import ABC
from transducers.interfaces.abstract_transducer import AbstractTransducer
from typing import Optional
from enumerations import SensorMeasure
from enumerations import MeasurementUnit
from enumerations import MeasureType
from measure_instruments import SensorData
from typing import List
from misc import Validate


class Sensor(AbstractTransducer, ABC):

    def __init__(self, name: str,  measure: SensorMeasure, unit: MeasurementUnit, measure_type: MeasureType,
                 data_frequency: float, current_value: Optional[float] = None):
        """
        :param name: the unique name of a sensor
        :param measure: the phenomenom (e.g., temperature) this sensor measures
        :param unit: the measurement unit of the data being measured
        :param measure_type: the type of data measured by the sensor
        :param data_frequency: what interval is the data recorded
        :param current_value: the current value for the sensor
        """
        super().__init__(name)
        self._measure = None
        self._data_frequency = None
        self._unit = None
        self._current_value = current_value
        self._measure_type = None
        self._data: [SensorData] = []

        # Setting values using setters to perform validation
        self.measure = measure
        self.data_frequency = data_frequency
        self.unit = unit
        self.measure_type = measure_type

        # validate sensor type and measurement
        if not Validate.validate_sensor_type(self.measure.value, self.unit.value):
            raise ValueError("{0} sensor can not have {1} measurement unit".format(measure.value, unit.value))

    @property
    def measure(self) -> SensorMeasure:
        return self._measure

    @measure.setter
    def measure(self, value: SensorMeasure):
        if value is not None:
            self._measure = value
        else:
            raise ValueError("measure must be of type SensorMeasure")

    @property
    def data_frequency(self) -> float:
        return self._data_frequency

    @data_frequency.setter
    def data_frequency(self, value: float):
        if value is not None:
            self._data_frequency = value
        else:
            raise ValueError("data_frequency must be float")

    @property
    def unit(self) -> MeasurementUnit:
        return self._unit

    @unit.setter
    def unit(self, value: MeasurementUnit):
        if value is not None:
            self._unit = value
        else:
            raise ValueError("unit must be of type MeasurementUnit")

    @property
    def current_value(self) -> float:
        return self._current_value

    @current_value.setter
    def current_value(self, value: float):
       self._current_value = value

    @property
    def measure_type(self) -> MeasureType:
        return self._measure_type

    @property
    def data(self) -> List[SensorData]:
        return self._data

    @measure_type.setter
    def measure_type(self, value: MeasureType):
        if value is not None:
            self._measure_type = value
        else:
            raise ValueError("measure_type must be of type MeasureType")

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
            f"CurrentValue: {self.current_value}, "
            f"Measure Type: {self.measure_type}\n"
            f"Data Count: {len(sensor_data)}\n"
            f"Data: {sensor_data})"
        )