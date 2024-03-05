from datetime import datetime
import uuid
from abc import ABC
from misc import Validate


class AbstractDataMeasure(ABC):
    """
    This class represents the data recorded by sensors and meters
    The unit of measurement depends on the phenomenon measured by a meter or sensor

    Author: Peter Yefi
    Email: peteryefi@gmail.com
    """

    def __init__(self, value: float, timestamp: str = None):
        """
        :param value: The numerical value measured

        """
        self._UID = uuid.uuid4()
        self._timestamp = datetime.now() if timestamp is None else Validate.parse_date(timestamp)
        self._value = None

        # Apply validation
        self.value = value

    @property
    def UID(self):
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
    def timestamp(self) -> datetime:
        return self._timestamp

    def __str__(self):
        """
        :return: A formatted string of the meter readings.
        """
        return (f"DataMeasure (UID: {self.UID}, Value: {self.value}, "
                f"Timestamp: {self.timestamp})")

