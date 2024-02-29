from unittest import TestCase
from measure_instruments import Meter
from measure_instruments import MeterMeasure
from enumerations import MeasurementUnit
from enumerations import MeterType


class TestMeter(TestCase):

    def setUp(self) -> None:

        self.meter = Meter("huz.cab.err", "Honeywell", 5, MeasurementUnit.KILOWATTS, MeterType.POWER)

    def test_meter_without_manufacture(self):
        try:
            self.assertEqual(self.meter.meter_location, "huz.cab.err")
            self.assertEqual(self.meter.meter_type, MeterType.POWER)
            self.assertEqual(self.meter.measurement_unit.KILOWATTS.value, "kW")
            self.meter.manufacturer = None
        except ValueError as err:
            self.assertEqual(err.__str__(), "Manufacturer must be a string")

    def test_power_data_with_wrong_value(self):
        try:
            MeterMeasure("25")
        except ValueError as err:
            self.assertEqual(err.__str__(), "Value must be a float")

    def test_power_meter_with_data(self):
        self.meter.manufacturer = "Honeywell"
        power_values = [2.5, 3.8, 9.7, 3.5]
        for power in power_values:
            self.meter.add_meter_measure(power)
        self.assertEqual(len(self.meter.meter_measures), 4)
        self.assertEqual(self.meter.meter_measures[0].value, 2.5)
        self.assertIsNotNone(self.meter.meter_measures[0].UID)



