from datetime import datetime
import uuid
from abc import ABC
from metamenth.misc import Validate
from metamenth.enumerations import DataMeasurementType
from typing import Union


class AbstractDataMeasure(ABC):
    """
    This class represents the data recorded by sensors and meters
    The unit of measurement depends on the phenomenon measured by a meter or sensor

    Author: Peter Yefi
    Email: peteryefi@gmail.com
    """

    def __init__(self, value: Union[float, str], timestamp: str = None, measurement_type: DataMeasurementType = None):
        """
        :param value: The numerical/string value measured
        :param timestamp: the time of measurement
        :param measurement_type: the type of the measurment, e.g., electricity consumption

        """
        self._UID = str(uuid.uuid4())
        self._timestamp = datetime.now().replace(microsecond=0) if timestamp is None else Validate.parse_date(timestamp)
        self._value = None
        self._measurement_type = measurement_type

        # Apply validation
        self.value = value

    @property
    def UID(self) -> str:
        return self._UID

    @property
    def value(self) -> float:
        return self._value

    @value.setter
    def value(self, value: float):
        if value is not None:
            self._value = value
        else:
            raise ValueError("Value must be a float")

    @property
    def measurement_type(self) -> DataMeasurementType:
        return self._measurement_type

    @measurement_type.setter
    def measurement_type(self, value: DataMeasurementType):
        self._measurement_type = value


    @property
    def timestamp(self) -> datetime:
        return self._timestamp

    def __str__(self):
        """
        :return: A formatted string of the meter readings.
        """
        return (f"DataMeasure (UID: {self.UID}, Value: {self.value}, "
                f"Timestamp: {self.timestamp}, Measurement Type: {self.measurement_type.value if self.measurement_type else None})")

