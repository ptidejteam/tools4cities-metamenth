from enumerations import MeterType
from enumerations import MeasurementUnit
from enumerations import MeterMeasureMode
from measure_instruments.meter_measure import MeterMeasure
from enumerations import MeterAccumulationFrequency
from typing import Dict
from utils import StructureEntitySearch
from measure_instruments.interfaces.abstract_reader import AbstractReader


class EVChargingMeter(AbstractReader):
    """
    A representation of an electric vehicle charging meter

    Author: Peter Yefi
    Email: peteryefi@gmail.com
    """

    def __init__(self, meter_location: str, measurement_unit: MeasurementUnit,
                 manufacturer: str = None):
        """
        Initializes a Meter instance.

        :param meter_location: The what3word location of the meter.
        :param manufacturer: The manufacturer of the meter.
        :param measurement_unit: The measurement unit of the meter data.
        """
        super().__init__(measurement_unit, meter_location, manufacturer)

    def __str__(self):
        """
        :return: A formatted string representing the meter.
        """

        return (
            f"EVChargingMeter("
            f"{super().__str__()})"
        )
