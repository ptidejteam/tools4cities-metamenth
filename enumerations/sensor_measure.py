from enum import Enum


class SensorMeasure(Enum):
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
    NOISE = "Noise"
    ENERGY = "Energy"
    GLOBAL_RADIATION = "GlobalRadiation"
    DIRECT_RADIATION = "DirectRadiation"
    POWER = "Power"
    SMOKE = "Smoke"
    OCCUPANCY = "Occupancy"
    DAYLIGHT = "Daylight"
    AIR_VOLUME = "AirVolume"
    OTHER = "Other"
