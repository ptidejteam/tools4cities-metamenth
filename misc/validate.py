from typing import Dict
from enumerations import SensorMeasure
from enumerations import MeasurementUnit
from datetime import datetime
from enumerations import EngineType
from enumerations import EngineSubType


class Validate:
    """
    Has miscillineous methods for validation

    """

    @staticmethod
    def validate_what3word(input_string: str) -> str:
        """
        Validates that a string is delimited by two "." with three words.

        :param input_string: The string to be validated.
        :return: the input string if valid else raises an error
        """

        if input_string is None or "":
            return ""
        # Split the string using "." as a delimiter
        parts = input_string.split(".")

        # Check if there are exactly three parts
        if len(parts) == 3 and all(part.strip() for part in parts):
            return input_string
        else:
            raise ValueError("Location should be a string of three words delimited with two periods.")

    @staticmethod
    def validate_solar_heat_gain_coefficient(value: float) -> float:
        if value is not None:
            if 0 <= value <= 1:
                return value
            else:
                raise ValueError("Solar Heat Gain Coefficient must be a float between 0 and 1.")

    @staticmethod
    def validate_none(attributes: Dict):
        none_variables = ""

        for attribute_name, attribute_type in attributes.items():
            if attribute_type is None:
                none_variables = none_variables + attribute_name + " "

        if none_variables:
            raise ValueError("{0} is/are mandatory".format(none_variables.rstrip()))

    @staticmethod
    def parse_date(date_string):
        """
        Returns datetime in the format YYYY-MM-DD HH:MM:SS
        :param date_string: the data string
        :return:
        """
        formats = [
            '%Y-%m-%d %H:%M',
            '%Y-%m-%d',
            '%Y/%m/%d %H:%M:%S.%f',
            '%y/%m/%d %H:%M:%S.%f',
            '%Y/%m/%d %H:%M:%S',
            '%Y/%m/%d %H:%M',
            '%Y/%m/%d',
            '%m/%d/%Y %H:%M',
            '%Y-%m-%d %H:%M:%S.%f',
            '%Y-%m-%d %H:%M:%S'
            ]
        for fmt in formats:
            try:
                dt = datetime.strptime(date_string, fmt)
                return dt.replace(microsecond=0)  # Truncate milliseconds
            except ValueError as err:
                pass
        raise ValueError("No valid date format found")

    @staticmethod
    def validate_sensor_type(sensor_measure: str, unit: str) -> bool:
        """
        Validates the unit of measurement and the type of sensor
        e.g., a temperature sensor should have degree celsius as the measurement unit
        :param sensor_measure: the type of sensor e.g., temperature sensor
        :param unit: the unit of measurement for the type of sensor
        :return: true if the correct unit is used for a specific sensor else false
        Always returns true if sensor measure is other
        """
        if sensor_measure == SensorMeasure.TEMPERATURE.value:
            if unit == MeasurementUnit.DEGREE_CELSIUS.value:
                return True
        elif sensor_measure == SensorMeasure.PRESSURE.value:
            if unit == MeasurementUnit.PASCAL.value:
                return True
        elif sensor_measure == SensorMeasure.CARBON_DIOXIDE.value:
            if unit == MeasurementUnit.PARTS_PER_MILLION.value:
                return True
        elif sensor_measure == SensorMeasure.AIR_VOLUME.value:
            if unit in [MeasurementUnit.LITER.value, MeasurementUnit.CUBIC_FEET.value,
                        MeasurementUnit.CUBIC_CENTIMETER.value, MeasurementUnit.CUBIC_METER.value]:
                return True
        elif sensor_measure in [SensorMeasure.GAS_VELOCITY.value, SensorMeasure.LIQUID_VELOCITY.value]:
            if unit in [MeasurementUnit.METERS_PER_SECOND.value, MeasurementUnit.FEET_PER_SECOND.value]:
                return True
        elif sensor_measure == SensorMeasure.DAYLIGHT.value:
            if unit == MeasurementUnit.LUX.value:
                return True
        elif sensor_measure in [SensorMeasure.DIRECT_RADIATION.value, SensorMeasure.GLOBAL_RADIATION.value]:
            if unit == MeasurementUnit.WATTS_PER_METER_SQUARE.value:
                return True
        elif sensor_measure == SensorMeasure.LUMINANCE.value:
            if unit in [MeasurementUnit.CANDELA_PER_SQUARE_METER.value or MeasurementUnit.NITS.value]:
                return True
        elif sensor_measure == SensorMeasure.NOISE.value:
            if unit == MeasurementUnit.DECIBELS.value:
                return True
        elif sensor_measure == SensorMeasure.OCCUPANCY.value:
            if unit == MeasurementUnit.PRESENCE.value:
                return True
        elif sensor_measure == SensorMeasure.SMOKE.value:
            if unit == MeasurementUnit.MICROGRAM_PER_CUBIC_METER.value:
                return True
        elif sensor_measure == SensorMeasure.CURRENT.value:
            if unit == MeasurementUnit.AMPERE.value:
                return True
        elif sensor_measure == SensorMeasure.VOLTAGE.value:
            if unit == MeasurementUnit.VOLT.value:
                return True
        elif sensor_measure == SensorMeasure.HUMIDITY.value:
            if unit == MeasurementUnit.RELATIVE_HUMIDITY.value:
                return True
        elif sensor_measure == SensorMeasure.OTHER.value:
            return True
        return False

    @staticmethod
    def validate_engine_fuel(self, engine_type: str, engine_sub_type: str) -> bool:
        """
        Validates engine type and fuel used by such engine types
        """
        if engine_type == EngineType.FUEL_CELL.value:
            if engine_sub_type in [EngineSubType.HYDROGEN.value]:
                return True
        elif engine_type == EngineType.STIRLING.value:
            if engine_sub_type in [EngineSubType.NATURAL_GAS.value, EngineSubType.PROPANE.value,
                                   EngineSubType.BIO_DIESEL.value, EngineSubType.GEO_THERMAL.value,
                                   EngineSubType.ETHANOL.value]:
                return True
        elif engine_type == EngineType.INTERNAL_COMBUSTION.value:
            if engine_sub_type in [EngineSubType.GASOLINE.value, EngineSubType.NATURAL_GAS.value,
                                   EngineSubType.ETHANOL.value, EngineSubType.DIESEL.value,
                                   EngineSubType.BIO_DIESEL.value, EngineSubType.JETFUEL.value]:
                return True
        elif engine_type == EngineType.STEAM.value:
            if engine_sub_type in [EngineSubType.OIL.value, EngineSubType.PEAT.value, EngineSubType.WOOD.value,
                                   EngineSubType.CHARCOAL.value, EngineSubType.COAL.value,
                                   EngineSubType.NATURAL_GAS.value, EngineSubType.BIOMASS.value,
                                   EngineSubType.GEO_THERMAL.value]:
                return True
        elif engine_type == EngineType.ELECTROLYSER.value:
            if engine_sub_type is None:
                return True

        elif engine_type == EngineType.MICRO_TURBINE.value:
            if engine_sub_type in [EngineSubType.NATURAL_GAS.value, EngineSubType.DIESEL.value,
                                   EngineSubType.PROPANE.value, EngineSubType.BIO_DIESEL, EngineSubType.HYDROGEN.value,
                                   EngineSubType.JETFUEL.value]:
                return True
        return False



