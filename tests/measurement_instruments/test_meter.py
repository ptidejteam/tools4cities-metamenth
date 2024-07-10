from unittest import TestCase
from measure_instruments.meter import Meter
from enumerations import MeasurementUnit
from enumerations import MeterType
from enumerations import MeterMeasureMode
from enumerations import MeterAccumulationFrequency
from measure_instruments.meter import MeterMeasure
from measure_instruments.ev_charging_meter import EVChargingMeter
from measure_instruments.electric_vehicle_connectivity import ElectricVehicleConnectivity
from enumerations import OperationType
from uuid import uuid4


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

    def test_ev_charging_meter_with_data(self):
        ev_charging_meter = EVChargingMeter("huz.cab.err", MeasurementUnit.KILOWATTS)
        charging_data_one = ElectricVehicleConnectivity(1.5, "2024-06-15 16:00:00",
                                                        "2024-06-15 18:00:00", OperationType.CHARGING,
                                                        str(uuid4()))
        charging_data_two = ElectricVehicleConnectivity(2.8, "2024-06-15 13:00:00",
                                                        "2024-06-15 14:00:00", OperationType.CHARGING,
                                                        str(uuid4()))
        discharging_data = ElectricVehicleConnectivity(0.8, "2024-07-09 19:00:00",
                                                       "2024-07-09 20:00:00", OperationType.DISCHARGING,
                                                       str(uuid4()))

        ev_charging_meter.add_meter_measure(charging_data_one)
        ev_charging_meter.add_meter_measure(charging_data_two)
        ev_charging_meter.add_meter_measure(discharging_data)

        self.assertEqual(ev_charging_meter.measurement_unit, MeasurementUnit.KILOWATTS)
        self.assertEqual(len(ev_charging_meter.get_connectivity_data()), 3)
        self.assertEqual(len(ev_charging_meter.get_connectivity_data({
            'operation_type': OperationType.DISCHARGING.value})), 1)
        self.assertEqual(ev_charging_meter.get_connectivity_data({'operation_type': OperationType.DISCHARGING.value})[0],
                         discharging_data)



