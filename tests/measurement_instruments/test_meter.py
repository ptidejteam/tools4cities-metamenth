from unittest import TestCase
from measure_instruments.meter import Meter
from enumerations import MeasurementUnit
from enumerations import MeterType
from enumerations import MeterMeasureMode
from enumerations import MeterAccumulationFrequency
from measure_instruments.meter import MeterMeasure


class TestMeter(TestCase):

    def setUp(self) -> None:

        self.meter = Meter(meter_location="huz.cab.err", manufacturer="Honeywell", measurement_frequency=5,
                           measurement_unit=MeasurementUnit.KILOWATTS, meter_type=MeterType.ELECTRICITY,
                           measure_mode=MeterMeasureMode.AUTOMATIC)

    def test_meter_without_manufacturer(self):
        try:
            self.assertEqual(self.meter.meter_location, "huz.cab.err")
            self.assertEqual(self.meter.meter_type, MeterType.ELECTRICITY)
            self.assertEqual(self.meter.measurement_unit.KILOWATTS.value, "kW")
            self.meter.manufacturer = None
        except ValueError as err:
            self.assertEqual(err.__str__(), "Manufacturer must be a string")

    def test_power_meter_with_accumulated_data_without_frequency(self):
        try:
            self.meter.data_accumulated = True
        except ValueError as err:
            self.assertEqual(err.__str__(), "accumulation_frequency must be a greater than 0")

    def test_power_meter_with_accumulated_data(self):
        try:
            self.meter.data_accumulated = True
            self.meter.accumulation_frequency = MeterAccumulationFrequency.DAILY
        except ValueError as err:
            self.assertEqual(err.__str__(), "accumulation_frequency must be a greater than 0")

    def test_power_meter_with_data(self):
        self.meter.manufacturer = "Honeywell"
        power_values = [2.5, 3.8, 9.7, 3.5]
        for power in power_values:
            self.meter.add_meter_measure(MeterMeasure(power))
        self.assertEqual(len(self.meter.get_meter_measures()), 4)
        self.assertEqual(self.meter.get_meter_measures()[0].value, 2.5)
        self.assertIsNotNone(self.meter.get_meter_measures()[0].UID)



