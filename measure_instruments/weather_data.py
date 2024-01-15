from datatypes import BinaryMeasure
from enumerations import WeatherValueType
from datetime import datetime
from uuid import uuid4


class WeatherData:
    def __init__(self, value: BinaryMeasure, value_type: WeatherValueType):
        """
        :param value: The binary measure (value and unit) of the weather data.
        :param value_type: The type of weather data e.g., humidity.
        """
        self.UID = str(uuid4())  # Generating a unique identifier
        self.timestamp = datetime.now()
        self.value = value
        self.value_type = value_type

    def __str__(self):
        """
        Returns a string representation of the BuildingWeatherData instance.

        :return: A formatted string representing the BuildingWeatherData details.
        """
        return (
            f"BuildingWeatherData("
            f"UID: {self.UID}, "
            f"Timestamp: {self.timestamp}, "
            f"Value: {self.value.value}, "
            f"ValueType: {self.value_type.value})"
        )