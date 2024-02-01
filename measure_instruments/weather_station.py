from uuid import uuid4
from measure_instruments import WeatherData
from typing import List
from misc import Validate


class WeatherStation:
    def __init__(self, location: str = None):
        """
        :param location: The location of the weather station.
        """
        self._UID = str(uuid4())
        self._location = Validate.validate_what3word(location)
        self._weather_data: List[WeatherData] = []

    @property
    def UID(self) -> str:
        return self._UID

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
        # Weather stations are equal if they share the same UID
        if isinstance(other, WeatherStation):
            # Check for equality based on the 'UID' attribute
            return self.UID == other.UID
        return False

    def __str__(self):
        weather_station_details = (
            f"WeatherStation("
            f"UID: {self.UID}, "
            f"Location: {self.location}, "
            f"WeatherData Count: {len(self.weather_data)})"
        )
        weather_data = "\n".join(str(data) for data in self.weather_data)
        return f"{weather_station_details}\nWeather Data:\n{weather_data}"
