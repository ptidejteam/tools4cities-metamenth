from uuid import uuid4
from metamenth.measure_instruments.weather_data import WeatherData
from typing import List
from metamenth.misc import Validate
from typing import Dict
from metamenth.utils import StructureEntitySearch


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

    def add_weather_data(self, weather_data: [WeatherData]):
        """
        Adds some data recordings to this WeatherStation.
        :param weather_data: some weather data recorded for the weather station.
        """
        self._weather_data.extend(weather_data)

    def get_weather_data(self, search_terms: Dict = None) -> [WeatherData]:
        """
        Search weather data by attributes values
        :param search_terms: a dictionary of attributes and their values
        :return [WeatherData]:
        """
        return StructureEntitySearch.search(self._weather_data, search_terms)

    def get_weather_data_by_date(self, from_timestamp: str, to_timestamp: str = None) ->[WeatherData]:
        """
        searches weather data based on provided timestamp
        :param from_timestamp: the start timestamp
        :param to_timestamp: the end timestamp
        :return: [WeatherData]
        """
        return StructureEntitySearch.date_range_search(self._weather_data, from_timestamp, to_timestamp)

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
            f"WeatherData Count: {len(self._weather_data)})"
        )
        weather_data = "\n".join(str(data) for data in self._weather_data)
        return f"{weather_station_details}\nWeather Data:\n{weather_data}"
