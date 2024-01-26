from datatypes.binary_measure import BinaryMeasure
from enumerations import WeatherValueType
from datetime import datetime
from uuid import uuid4
from misc import Validate
from datatypes.interfaces import AbstractMeasure


class WeatherData:
    def __init__(self, data: AbstractMeasure):
        """
        :param data: The binary measure (value and unit) of the weather data.
        """
        Validate.validate_none({"Data": data})
        self._UID = str(uuid4())  # Generating a unique identifier
        self._timestamp = datetime.now()
        self._data = data

    @property
    def UID(self) -> str:
        return self._UID

    @property
    def data(self) -> AbstractMeasure:
        return self._data

    @data.setter
    def data(self, value: AbstractMeasure):
        self._data = value

    @property
    def timestamp(self) -> datetime:
        return self._timestamp

    def __str__(self):
        """
        Returns a string representation of the BuildingWeatherData instance.

        :return: A formatted string representing the BuildingWeatherData details.
        """
        return (
            f"BuildingWeatherData("
            f"UID: {self.UID}, "
            f"Timestamp: {self.timestamp}, "
            f"Data: {self.data})"
        )
