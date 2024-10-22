from datetime import datetime
from uuid import uuid4
from metamenth.datatypes.interfaces.abstract_measure import AbstractMeasure
from metamenth.misc import Validate


class WeatherData:
    def __init__(self, data: AbstractMeasure, timestamp: str = None):
        """
        :param data: The binary measure (value and unit) of the weather data.

        """
        self._UID = str(uuid4())  # Generating a unique identifier
        self._timestamp = datetime.now().replace(microsecond=0) if timestamp is None else Validate.parse_date(timestamp)
        self._data = None

        self.data = data

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
