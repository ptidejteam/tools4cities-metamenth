from unittest import TestCase
from misc import MeasureFactory
from enumerations import RecordingType
from datatypes.measure import Measure
from enumerations import MeasurementUnit
from transducers.sensor import Sensor
from enumerations import SensorMeasure
from enumerations import MeasureType


class TestSensor(TestCase):

    def setUp(self) -> None:
        self.density_measure = MeasureFactory.create_measure(RecordingType.BINARY.value,
                                                             Measure(MeasurementUnit.KILOGRAM_PER_CUBIC_METER, 0.5))
        self.hc_measure = MeasureFactory.create_measure(RecordingType.BINARY.value,
                                                        Measure(MeasurementUnit.JOULES_PER_KELVIN, 4.5))
        self.tt_measure = MeasureFactory.create_measure(RecordingType.BINARY.value,
                                                        Measure(MeasurementUnit.WATTS_PER_SQUARE_METER_KELVIN, 2.5))
        self.material = None

    def test_temperature_sensor_with_no_measure_frequency(self):
        try:
            Sensor("TEMP.SENSOR", SensorMeasure.TEMPERATURE, MeasurementUnit.DEGREE_CELSIUS,
                   MeasureType.THERMO_COUPLE_TYPE_A, None)
        except ValueError as err:
            print(err)
            self.assertEqual(err.__str__(), "data_frequency must be float")

    def test_co2_sensor_with_temperature_measurement(self):
        try:
            Sensor("CO2.SENSOR", SensorMeasure.CARBON_DIOXIDE, MeasurementUnit.DEGREE_CELSIUS,
                   MeasureType.THERMO_COUPLE_TYPE_A, 5)
        except ValueError as err:
            self.assertEqual(err.__str__(), "CarbonDioxide sensor can not have DegreeCelsius (°C) measurement unit")

    def test_pressure_sensor_with_gas_velocity_measurement(self):
        try:
            Sensor("PRESSURE.SENSOR", SensorMeasure.PRESSURE, MeasurementUnit.METERS_PER_SECOND,
                   MeasureType.THERMO_COUPLE_TYPE_A, 5)
        except ValueError as err:
            self.assertEqual(err.__str__(), "Pressure sensor can not have MetersPerSecond (m/s) measurement unit")

    def test_air_volume_sensor_with_luminance_measurement(self):
        try:
            Sensor("AIR.VOLUME.SENSOR", SensorMeasure.AIR_VOLUME, MeasurementUnit.CANDELA_PER_SQUARE_METER,
                   MeasureType.THERMO_COUPLE_TYPE_A, 5)
        except ValueError as err:
            print(err)
            self.assertEqual(err.__str__(),
                             "AirVolume sensor can not have CandelaPerSquareMeter (cd/m2) measurement unit")

    def test_smoke_sensor_with_noise_measurement(self):
        try:
            Sensor("SMOKE.SENSOR", SensorMeasure.SMOKE, MeasurementUnit.DECIBELS,
                   MeasureType.THERMO_COUPLE_TYPE_A, 5)
        except ValueError as err:
            self.assertEqual(err.__str__(), "Smoke sensor can not have Decibels (dB) measurement unit")

    def test_current_sensor_with_60_seconds_data_interval(self):
        current_sensor = Sensor("CURRENT.SENSOR", SensorMeasure.CURRENT, MeasurementUnit.AMPERE,
                                MeasureType.THERMO_COUPLE_TYPE_A, 60)
        self.assertEqual(current_sensor.data_frequency, 60)
        self.assertEqual(current_sensor.measure.value, SensorMeasure.CURRENT.value)
        self.assertEqual(current_sensor.change_of_value, False)
        self.assertEqual(current_sensor.meta_data, {})

    def test_cov_smoke_sensor_with_metadata(self):
        smoke_sensor = Sensor("SMOKE.SENSOR", SensorMeasure.SMOKE, MeasurementUnit.MICROGRAM_PER_CUBIC_METER,
                              MeasureType.THERMO_COUPLE_TYPE_B, 10)
        self.assertEqual(smoke_sensor.data_frequency, 10)
        smoke_sensor.change_of_value = True
        self.assertEqual(smoke_sensor.change_of_value, True)

        metadata = {'default_data_interval': 10, 'description': 'change of value based on peak threshold'}
        smoke_sensor.meta_data = metadata
        self.assertEqual(smoke_sensor.meta_data, metadata)
        self.assertEqual(smoke_sensor.meta_data['default_data_interval'], 10)

    def test_co2_sensor_with_current_value(self):
        co2_sensor = Sensor("CO2.SENSOR", SensorMeasure.CARBON_DIOXIDE, MeasurementUnit.PARTS_PER_MILLION,
                            MeasureType.THERMO_COUPLE_TYPE_B, 70)
        co2_sensor.current_value = 0.389
        self.assertEqual(co2_sensor.current_value, 0.389)
        self.assertEqual(co2_sensor.measure, SensorMeasure.CARBON_DIOXIDE)

    def test_direct_radiation_sensor_with_input_voltage_rage(self):
        rad_sensor = Sensor("DIR.RADIATION.SENSOR", SensorMeasure.DIRECT_RADIATION,
                            MeasurementUnit.WATTS_PER_METER_SQUARE,
                            MeasureType.THERMO_COUPLE_TYPE_B, 70)
        input_voltage_range = MeasureFactory.create_measure(RecordingType.CONTINUOUS.value,
                                                            Measure(MeasurementUnit.VOLT, 0.5, 0.8))
        rad_sensor.input_voltage_range = input_voltage_range
        self.assertEqual(rad_sensor.input_voltage_range, input_voltage_range)
        self.assertEqual(rad_sensor.input_voltage_range.measurement_unit, MeasurementUnit.VOLT)
        self.assertEqual(rad_sensor.input_voltage_range.minimum, 0.5)
        self.assertEqual(rad_sensor.input_voltage_range.maximum, 0.8)
        self.assertEqual(rad_sensor.input_voltage_range.measure_type, None)

    def test_daylight_sensor_with_output_current_rage(self):
        daylight_sensor = Sensor("DAYLIGHT.SENSOR", SensorMeasure.DAYLIGHT,
                                 MeasurementUnit.LUX,
                                 MeasureType.THERMO_COUPLE_TYPE_C, 70)
        output_current_range = MeasureFactory.create_measure(RecordingType.CONTINUOUS.value,
                                                             Measure(MeasurementUnit.AMPERE, 0.023, 0.017))
        daylight_sensor.output_current_range = output_current_range
        self.assertEqual(daylight_sensor.output_current_range, output_current_range)
        self.assertEqual(daylight_sensor.output_current_range.measurement_unit, MeasurementUnit.AMPERE)
        self.assertEqual(daylight_sensor.output_current_range.minimum, 0.023)
        self.assertEqual(daylight_sensor.output_current_range.maximum, 0.017)
        self.assertEqual(daylight_sensor.input_current_range, None)
        self.assertEqual(daylight_sensor.input_voltage_range, None)
        self.assertEqual(daylight_sensor.output_voltage_range, None)
