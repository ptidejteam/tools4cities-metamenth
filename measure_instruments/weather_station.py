from uuid import uuid4
from measure_instruments.weather_data import WeatherData
from typing import List
from misc import Validate


class WeatherStation:
    def __init__(self, name: str, location: str = None):
        """
        :param location: The location of the weather station.
        """
        self._UID = str(uuid4())
        self._name = None
        self._location = Validate.validate_what3word(location)
        self._weather_data: List[WeatherData] = []

        self.name = name

    @property
    def UID(self) -> str:
        return self._UID

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        if value is not None:
            self._name = value
        else:
            ValueError('name must be of type str')

    @property
    def location(self) -> str:
        return self._location

    @location.setter
    def location(self, value: str):
        self._location = Validate.validate_what3word(value)

    @property
    def weather_data(self) -> List[WeatherData]:
        return self._weather_data

    def add_weather_data(self, weather_data: [WeatherData]):
        """
        Adds some data recordings to this WeatherStation.
        :param weather_data: some weather data recorded for the weather station.
        """
        self.weather_data.extend(weather_data)

    def __eq__(self, other):
        # Weather stations are equal if they share the same name
        if isinstance(other, WeatherStation):
            # Check for equality based on the 'name' attribute
            return self.name == other.name
        return False

    def __str__(self):
        weather_station_details = (
            f"WeatherStation("
            f"UID: {self.UID}, "
            f"UID: {self.name}, "
            f"Location: {self.location}, "
            f"WeatherData Count: {len(self.weather_data)})"
        )
        weather_data = "\n".join(str(data) for data in self.weather_data)
        return f"{weather_station_details}\nWeather Data:\n{weather_data}"
