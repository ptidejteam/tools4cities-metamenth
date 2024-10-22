from metamenth.transducers.interfaces.abstract_transducer import AbstractTransducer
from typing import Optional
from metamenth.enumerations import SensorMeasure
from metamenth.enumerations import MeasurementUnit
from metamenth.enumerations import SensorMeasureType
from metamenth.misc import Validate
from metamenth.datatypes.interfaces.abstract_range_measure import AbstractRangeMeasure
from metamenth.enumerations import SensorLogType
from metamenth.datatypes.interfaces.abstract_measure import AbstractMeasure


class Sensor(AbstractTransducer):

    def __init__(self, name: str, measure: SensorMeasure, unit: MeasurementUnit, measure_type: SensorMeasureType,
                 data_frequency: float, current_value: Optional[float] = None,
                 measure_range: AbstractRangeMeasure = None, sensor_log_type: SensorLogType = SensorLogType.POLLING):
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
        self._measure_range = measure_range
        self._sensor_log_type = sensor_log_type

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
    def measure_range(self) -> AbstractRangeMeasure:
        return self._measure_range

    @measure_range.setter
    def measure_range(self, value: AbstractRangeMeasure):
        if value is not None:
            self._measure_range = value
        else:
            raise ValueError("measure must be of type AbstractRangeMeasure")

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
    def measure_type(self) -> SensorMeasureType:
        return self._measure_type

    @measure_type.setter
    def measure_type(self, value: SensorMeasureType):
        if value is not None:
            self._measure_type = value
        else:
            raise ValueError("measure_type must be of type MeasureType")

    @property
    def sensor_log_type(self) -> SensorLogType:
        return self._sensor_log_type

    @sensor_log_type.setter
    def sensor_log_type(self, value: SensorLogType):
        if value is not None:
            self._sensor_log_type = value
        else:
            raise ValueError("measure must be of type SensorLogType")

    @property
    def set_point(self) -> AbstractMeasure:
        return self._set_point

    @set_point.setter
    def set_point(self, value: AbstractMeasure):
        self.set_set_point(value, self._unit)

    def __str__(self):
        sensor_data = "\n".join(str(data) for data in self._data)
        return (
            f"Sensor("
            f"{super().__str__()}, "
            f"UID: {self.UID}, "
            f"Name: {self.name}, "
            f"Measure: {self.measure}, "
            f"Measure Range: {self.measure_range}, "
            f"Data Frequency: {self.data_frequency}, "
            f"Unit: {self.unit}, "
            f"CurrentValue: {self.current_value}, "
            f"Measure Type: {self.measure_type}, "
            f"Log Type: {self.sensor_log_type.value}, "
            f"Data Count: {len(sensor_data)}\n"
            f"Data: {sensor_data})"
        )