from unittest import TestCase
from metamenth.energysystem.engine import Engine
from metamenth.enumerations import MeterMeasureMode
from metamenth.enumerations import EngineType
from metamenth.enumerations import EngineSubType
from metamenth.enumerations import EngineMode
from metamenth.energysystem.solar_pv import SolarPV
from metamenth.enumerations import SolarPVType
from metamenth.enumerations import CellType
from metamenth.misc import MeasureFactory
from metamenth.enumerations import RecordingType
from metamenth.datatypes.measure import Measure
from metamenth.energysystem.wind_mill import WindMill
from metamenth.enumerations import WindTurbineType
from metamenth.datatypes.operational_schedule import OperationalSchedule
from datetime import datetime
from datetime import timedelta
from metamenth.energysystem.storage_system.battery import Battery
from metamenth.enumerations import BatteryTech
from metamenth.enumerations import EnergySource
from metamenth.energysystem.storage_system.electric_vehicle import ElectricVehicle
from metamenth.energysystem.storage_system.super_capacitor import SuperCapacitor
from metamenth.enumerations import V2GMode
from metamenth.enumerations import CapacitorTech
from metamenth.transducers.sensor import Sensor
from metamenth.enumerations import SensorMeasure
from metamenth.enumerations import SensorMeasureType
from metamenth.enumerations import SensorLogType
from metamenth.measure_instruments.meter import Meter
from metamenth.enumerations import MeasurementUnit
from metamenth.enumerations import MeterType
from metamenth.energysystem.electricals.uninterruptible_power_supply import UninterruptiblePowerSupply
from metamenth.enumerations import PowerState
from metamenth.enumerations import UPSPhase


class TestEnergySystems(TestCase):

    def setUp(self) -> None:
        pass

    def test_engine_without_type(self):
        try:
            _ = Engine("Gen Engine", True, MeasurementUnit.KILOWATTS_PER_HOUR,
                       None, EngineSubType.DIESEL, EngineMode.FUEL)
        except ValueError as err:
            self.assertEqual(err.__str__(), "engine_type should be of type EngineType")

    def test_fuel_cell_engine(self):
        engine = Engine("Gen Engine", True, MeasurementUnit.KILOWATTS_PER_HOUR,
                        EngineType.FUEL_CELL, EngineSubType.HYDROGEN, EngineMode.FUEL)
        self.assertEqual(engine.engine_type, EngineType.FUEL_CELL)
        self.assertEqual(engine.inverter, True)
        self.assertEqual(engine.engine_mode, EngineMode.FUEL)

    def test_engine_with_wrong_fuel_type(self):
        try:
            _ = Engine("Gen Engine", True, MeasurementUnit.KILOWATTS_PER_HOUR,
                       EngineType.FUEL_CELL, EngineSubType.BIO_DIESEL, EngineMode.FUEL)
        except ValueError as err:
            self.assertEqual(err.__str__(),
                             'EngineSubType.BIO_DIESEL is an invalid value for EngineType.FUEL_CELL')

    def test_create_solar_pv(self):
        solar_pv = SolarPV("Solar Panels", False, MeasurementUnit.WATTS,
                           SolarPVType.BUILDING_INTEGRATED_PHOTOVOLTAIC, CellType.AMORPHOUS)
        thermal_capacity = MeasureFactory.create_measure(RecordingType.BINARY.value,
                                                         Measure(MeasurementUnit.JOULES_PER_KELVIN, 2.3))
        solar_pv.thermal_capacity = thermal_capacity
        temp_sensor = Sensor("TEMPERATURE.SENSOR", SensorMeasure.TEMPERATURE, MeasurementUnit.DEGREE_CELSIUS,
                             SensorMeasureType.THERMO_COUPLE_TYPE_A, 900, sensor_log_type=SensorLogType.POLLING)
        voltage_sensor = Sensor("VOLTAGE.SENSOR", SensorMeasure.VOLTAGE, MeasurementUnit.VOLT,
                                SensorMeasureType.THERMO_COUPLE_TYPE_A, 900, sensor_log_type=SensorLogType.POLLING)
        solar_pv.add_transducer(temp_sensor)
        solar_pv.add_transducer(voltage_sensor)

        self.assertIsNone(solar_pv.module_area)
        self.assertEqual(solar_pv.thermal_capacity, thermal_capacity)
        self.assertEqual(solar_pv.solar_pv_type, SolarPVType.BUILDING_INTEGRATED_PHOTOVOLTAIC)
        self.assertEqual(len(solar_pv.get_transducers()), 2)
        self.assertEqual(solar_pv.get_transducer_by_uid(voltage_sensor.UID), voltage_sensor)

    def test_create_wind_mill_with_schedule(self):
        wind_mill = WindMill("Wind Mill", True, MeasurementUnit.MEGAWATTS, 4,
                             WindTurbineType.VERTICAL_AXIS_WIND_TURBINE_ON_SHORE)

        schedule = OperationalSchedule("WEEKDAYS", datetime.now(), datetime.now() + timedelta(days=5))

        wind_mill.schedulable_entity.add_schedule(schedule)
        wind_mill.manufacturer = "Vestas Wind Systems"
        wind_mill.model = "V90-2.0 MW"
        wind_mill.capacity = MeasureFactory.create_measure(RecordingType.BINARY.value,
                                                           Measure(MeasurementUnit.MEGAWATTS, 2))

        electricity_meter = Meter(meter_location="huz.cab.err",
                                  manufacturer="Honeywell",
                                  measurement_frequency=5,
                                  measurement_unit=MeasurementUnit.KILOWATTS_PER_HOUR,
                                  meter_type=MeterType.ELECTRICITY, measure_mode=MeterMeasureMode.AUTOMATIC)
        wind_mill.meter = electricity_meter

        self.assertEqual(wind_mill.capacity.value, 2)
        self.assertEqual(wind_mill.schedulable_entity.get_schedule_by_name("WEEKDAYS"), schedule)
        self.assertEqual(wind_mill.model, "V90-2.0 MW")
        self.assertEqual(wind_mill.meter, electricity_meter)

    def test_battery_storage_with_renewable_source(self):
        battery = Battery("Battery", True, MeasurementUnit.KILOWATTS_PER_HOUR, EnergySource.Renewable,
                          BatteryTech.LITHIUM)
        wind_mill = WindMill("Wind Mill", True, MeasurementUnit.MEGAWATTS, 4,
                             WindTurbineType.VERTICAL_AXIS_WIND_TURBINE_ON_SHORE)
        battery.add_renewable_energy_source(wind_mill)
        self.assertEqual(battery.schedulable_entity.get_schedules(), [])
        self.assertEqual(battery.energy_source, EnergySource.Renewable)
        self.assertEqual(battery.get_renewable_energy_source("Wind Mill"), wind_mill)

    def test_batter_storage_with_grid_source(self):
        battery = Battery("Battery", True, MeasurementUnit.KILOWATTS_PER_HOUR, EnergySource.GRID,
                          BatteryTech.NICKEL)
        battery.capacity = MeasureFactory.create_measure(RecordingType.BINARY.value,
                                                         Measure(MeasurementUnit.KILOWATTS_PER_HOUR, 24))
        self.assertEqual(battery.energy_source, EnergySource.GRID)
        self.assertEqual(battery.capacity.measurement_unit, MeasurementUnit.KILOWATTS_PER_HOUR)
        self.assertEqual(battery.capacity.value, 24)

    def test_create_electric_vehicle(self):
        ev = ElectricVehicle("EV", False, MeasurementUnit.KILOWATTS_PER_HOUR)
        ev.v2g_mode = V2GMode.PEAK_SHAVING
        ev.v2g_capability = True
        power_limit = MeasureFactory.create_measure(RecordingType.BINARY.value,
                                                    Measure(MeasurementUnit.KILOWATTS_PER_HOUR, 10))
        ev.v2g_power_limit = power_limit
        self.assertEqual(ev.v2g_mode, V2GMode.PEAK_SHAVING)
        self.assertEqual(ev.v2g_power_limit, power_limit)
        self.assertEqual(ev.capacity, None)

    def test_create_super_capacitor(self):
        sc = SuperCapacitor("SC", False, MeasurementUnit.KILOWATTS_PER_HOUR, EnergySource.GRID,
                            CapacitorTech.LITHIUM_IRON)

        self.assertNotEqual(sc.energy_source, EnergySource.Renewable)
        self.assertIsNone(sc.capacity)
        self.assertEqual(sc.technology, CapacitorTech.LITHIUM_IRON)

    def test_uninterruptible_power_supply_with_sensor_and_meter(self):
        ups = UninterruptiblePowerSupply("UPS.01", PowerState.ON, UPSPhase.SINGLE)
        voltage_meter = Meter(meter_location="huz.cab.err",
                              manufacturer="Honeywell",
                              measurement_frequency=5,
                              measurement_unit=MeasurementUnit.VOLT,
                              meter_type=MeterType.POWER, measure_mode=MeterMeasureMode.AUTOMATIC)
        voltage_sensor = Sensor("VOLTAGE.SENSOR", SensorMeasure.VOLTAGE, MeasurementUnit.VOLT,
                                SensorMeasureType.THERMO_COUPLE_TYPE_A, 900, sensor_log_type=SensorLogType.POLLING)
        ups.meter = voltage_meter
        ups.add_transducer(voltage_sensor)
        self.assertEqual(ups.power_rating, None)
        self.assertEqual(ups.get_transducers(), [voltage_sensor])
        self.assertEqual(ups.meter, voltage_meter)
