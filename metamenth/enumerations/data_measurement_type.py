"""
Copyright (c) 2023-2025 Peter Yefi.
All rights reserved. This program and the accompanying materials
are made available under the terms of the GNU General Public License v3.0
which accompanies this distribution, and is available at:
https://www.gnu.org/licenses/gpl-3.0.html

Contributors:
    Peter Yefi - API design and implementation
"""

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
