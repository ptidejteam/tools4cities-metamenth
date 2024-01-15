from enum import Enum


class WeatherValueType(Enum):
    """
    Different weather data a building weather station can record.

    Author: Peter Yefi
    Email: peteryefi@gmail.com
    """
    TEMPERATURE = "Temperature"
    HUMIDITY = "Humidity"
    RELATIVE_HUMIDITY = "RelativeHumidity"
    PRESSURE = "Pressure"
    PRECIPITATION = "Precipitation"
    WIND_SPEED = "WindSpeed"
    WIND_DIRECTOR = "WindDirection"
    MOISTURE_CONTENT = "MoistureContent"
    SOLAR_RADIATION = "SolarRadiation"
