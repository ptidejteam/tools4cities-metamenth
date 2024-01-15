from uuid import uuid4
from measure_instruments import WeatherData
from typing import List
from misc import Validate


class WeatherStation:
    def __init__(self, location: str = None):
        """
        :param location: The location of the weather station.
        """
        self.UID = str(uuid4())
        self.location = Validate.validate_what3word(location)
        self.weather_data: List[WeatherData] = []

    def add_weather_data(self, weather_data: [WeatherData]):
        """
        Adds some data recordings to this WeatherStation.
        :param weather_data: some weather data recorded for the weather station.
        """
        self.weather_data.extend(weather_data)

    def __str__(self):
        weather_station_details = (
            f"WeatherStation("
            f"UID: {self.UID}, "
            f"Location: {self.location}, "
            f"WeatherData Count: {len(self.weather_data)})"
        )
        weather_data = "\n".join(str(data) for data in self.weather_data)
        return f"{weather_station_details}\nWeather Data:\n{weather_data}"
