from enum import Enum


class DataMeasurementType(Enum):
    """
    Different weather data a building weather station can record.

    Author: Peter Yefi
    Email: peteryefi@gmail.com
    """
    OUTSIDE_TEMPERATURE = "OutsideTemperature"
    HUMIDITY = "Humidity"
    RELATIVE_HUMIDITY = "RelativeHumidity"
    PRESSURE = "Pressure"
    PRECIPITATION = "Precipitation"
    WIND_SPEED = "WindSpeed"
    WIND_DIRECTOR = "WindDirection"
    MOISTURE_CONTENT = "MoistureContent"
    SOLAR_RADIATION = "SolarRadiation"
    GLOBAL_NOMINAL_IRRADIANCE = "GlobalNominalIrradiance"
    DIFFUSE_HORIZONTAL_IRRADIANCE = "DiffuseHorizontalIrradiance"
    DIRECT_NOMINAL_IRRADIANCE = "DirectNominalIrradiance"
    GLOBAL_HORIZONTAL_IRRADIANCE = "GlobalHorizontalIrradiance"
    EXPORTED_ELECTRICITY = "ExportedElectricity"
    IMPORTED_ELECTRICITY = "ImportedElectricity"
    CONSUMED_ELECTRICITY = "ConsumedElectricity"
