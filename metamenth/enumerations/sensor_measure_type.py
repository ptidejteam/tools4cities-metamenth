from enum import Enum


class SensorMeasureType(Enum):
    """
    Various sensor measurement types

    Author: Peter Yefi
    Email: peteryefi@gmail.com
    """
    THERMO_COUPLE_TYPE_A = "ThermoCoupleTypeA"
    THERMO_COUPLE_TYPE_B = "ThermoCoupleTypeB"
    THERMO_COUPLE_TYPE_C = "ThermoCoupleTypeC"
    THERMO_COUPLE_TYPE_D = "ThermoCoupleTypeD"
    THERMO_COUPLE_TYPE_E = "ThermoCoupleTypeE"
    THERMO_COUPLE_TYPE_F = "ThermoCoupleTypeF"
    PT_100 = "PT100"
    PIEZO_RESISTIVE_PRESSURE = "PiezoResistivePressure"
    ANALOGUE_PRESSURE = "AnaloguePressure"
    PASSIVE_INFRARED = "PassiveInfrared"
