from unittest import TestCase
from energysystem.engine import Engine
from enumerations import MeasurementUnit
from enumerations import EngineType
from enumerations import EngineSubType
from enumerations import EngineMode
from energysystem.solar_pv import SolarPV
from enumerations import SolarPVType
from enumerations import CellType
from misc import MeasureFactory
from enumerations import RecordingType
from datatypes.measure import Measure
from energysystem.wind_mill import WindMill
from enumerations import WindTurbineType
from datatypes.operational_schedule import OperationalSchedule
from datetime import datetime
from datetime import timedelta
from energysystem.storage_system.battery import Battery
from enumerations import BatteryTech
from enumerations import EnergySource
from energysystem.storage_system.electric_vehicle import ElectricVehicle
from energysystem.storage_system.super_capacitor import SuperCapacitor
from enumerations import V2GMode
from enumerations import CapacitorTech


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
        self.assertIsNone(solar_pv.module_area)
        self.assertEqual(solar_pv.thermal_capacity, thermal_capacity)
        self.assertEqual(solar_pv.solar_pv_type, SolarPVType.BUILDING_INTEGRATED_PHOTOVOLTAIC)

    def test_create_wind_mill_with_schedule(self):
        wind_mill = WindMill("Wind Mill", True, MeasurementUnit.MEGAWATTS, 4,
                             WindTurbineType.VERTICAL_AXIS_WIND_TURBINE_ON_SHORE)

        schedule = OperationalSchedule("WEEKDAYS", datetime.now(), datetime.now() + timedelta(days=5))

        wind_mill.schedulable_entity.add_schedule(schedule)
        wind_mill.manufacturer = "Vestas Wind Systems"
        wind_mill.model = "V90-2.0 MW"
        wind_mill.capacity = MeasureFactory.create_measure(RecordingType.BINARY.value,
                                                           Measure(MeasurementUnit.MEGAWATTS, 2))
        self.assertEqual(wind_mill.capacity.value, 2)
        self.assertEqual(wind_mill.schedulable_entity.get_schedule_by_name("WEEKDAYS"), schedule)
        self.assertEqual(wind_mill.model, "V90-2.0 MW")

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

