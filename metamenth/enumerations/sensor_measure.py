from metamenth.enumerations.abstract_enum import AbstractEnum


class SensorMeasure(AbstractEnum):
    """
    Various phenomena that can be measured by a sensor

    Author: Peter Yefi
    Email: peteryefi@gmail.com
    """
    TEMPERATURE = "Temperature"
    PRESSURE = "Pressure"
    GAS_VELOCITY = "GasVelocity"
    LIQUID_VELOCITY = "LiquidVelocity"
    LUMINANCE = "Luminance"
    CARBON_DIOXIDE = "CarbonDioxide"
    CARBON_MONOXIDE = "CarbonMonoxide"
    NOISE = "Noise"
    CURRENT = "Current"
    VOLTAGE = "Voltage"
    GLOBAL_RADIATION = "GlobalRadiation"
    DIRECT_RADIATION = "DirectRadiation"
    SMOKE = "Smoke"
    OCCUPANCY = "Occupancy"
    DAYLIGHT = "Daylight"
    AIR_VOLUME = "AirVolume"
    HUMIDITY = "Humidity"
    OTHER = "Other"
