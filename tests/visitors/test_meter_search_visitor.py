from metamenth.structure.floor import Floor
from metamenth.enumerations import FloorType
from metamenth.structure.building import Building
from metamenth.enumerations import BuildingType
from metamenth.virtual.zone import Zone
from metamenth.enumerations import ZoneType
from metamenth.enumerations import HVACType
from tests.structure.base_test import BaseTest
from metamenth.visitors.meter_search_visitor import MeterSearchVisitor
from metamenth.enumerations import BoilerCategory
from metamenth.subsystem.hvac_components.boiler import Boiler
from metamenth.measure_instruments.meter import Meter
from metamenth.enumerations import MeasurementUnit
from metamenth.enumerations import MeterType
from metamenth.energysystem.electricals.uninterruptible_power_supply import UninterruptiblePowerSupply
from metamenth.enumerations import PowerState
from metamenth.enumerations import UPSPhase
from metamenth.enumerations import MeterMeasureMode
import copy
from metamenth.enumerations import RoomType


class TestSensorSearchVisitor(BaseTest):

    def test_search_meters_in_spaces(self):
        self.hall.add_transducer(self.presence_sensor)
        self.hall.add_transducer(self.temp_sensor)
        second_floor = Floor(self.floor_area, 2, FloorType.ROOFTOP, rooms=[self.hall])
        building = Building(2009, self.height, self.floor_area, self.internal_mass, self.address,
                            BuildingType.RESIDENTIAL, [self.floor, second_floor])

        electricity_meter_one = Meter(meter_location="huz.cab.err",
                                      manufacturer="Honeywell",
                                      measurement_frequency=5,
                                      measurement_unit=MeasurementUnit.KILOWATTS_PER_HOUR,
                                      meter_type=MeterType.ELECTRICITY, measure_mode=MeterMeasureMode.AUTOMATIC)

        electricity_meter_two = Meter(meter_location="huz.oof.err",
                                      manufacturer="Honeywell",
                                      measurement_frequency=10,
                                      measurement_unit=MeasurementUnit.KILOWATTS_PER_HOUR,
                                      meter_type=MeterType.ELECTRICITY, measure_mode=MeterMeasureMode.MANUAL)
        building.add_meter(electricity_meter_one)
        self.room.location = "huz.oof.err"
        self.room.meter = electricity_meter_two

        meter_search = MeterSearchVisitor(
            floor_criteria={'number': [1, 2]},
            meter_criteria={'meter_type': MeterType.ELECTRICITY.value})

        building.accept(meter_search)

        self.assertEqual(len(meter_search.found_entities), 2)
        self.assertIn(electricity_meter_one, meter_search.found_entities)
        self.assertIn(electricity_meter_two, meter_search.found_entities)
        self.assertEqual(meter_search.found_entities.count(electricity_meter_one), 1)

    def test_search_meters_with_unmatch_criteria(self):
        self.hall.add_transducer(self.presence_sensor)
        self.hall.add_transducer(self.temp_sensor)
        second_floor = Floor(self.floor_area, 2, FloorType.ROOFTOP, rooms=[self.hall])
        building = Building(2009, self.height, self.floor_area, self.internal_mass, self.address,
                            BuildingType.RESIDENTIAL, [self.floor, second_floor])

        electricity_meter_one = Meter(meter_location="huz.cab.err",
                                      manufacturer="Honeywell",
                                      measurement_frequency=5,
                                      measurement_unit=MeasurementUnit.KILOWATTS_PER_HOUR,
                                      meter_type=MeterType.ELECTRICITY, measure_mode=MeterMeasureMode.AUTOMATIC)

        building.add_meter(electricity_meter_one)

        meter_search = MeterSearchVisitor(
            floor_criteria={'number': 1},
            meter_criteria={'meter_type': [MeterType.POWER.value, MeterType.FLOW.value]})

        building.accept(meter_search)
        self.assertEqual(len(meter_search.found_entities), 0)

    def test_search_meters_in_spaces_hvac_components_and_energy_systems(self):
        self.hall.add_transducer(self.presence_sensor)
        self.hall.add_transducer(self.temp_sensor)
        second_floor = Floor(self.floor_area, 2, FloorType.ROOFTOP, rooms=[self.hall])
        building = Building(2009, self.height, self.floor_area, self.internal_mass, self.address,
                            BuildingType.RESIDENTIAL, [self.floor, second_floor])

        electricity_meter = Meter(meter_location="huz.cab.err",
                                  manufacturer="Honeywell",
                                  measurement_frequency=5,
                                  measurement_unit=MeasurementUnit.KILOWATTS_PER_HOUR,
                                  meter_type=MeterType.ELECTRICITY, measure_mode=MeterMeasureMode.AUTOMATIC)

        water_flow_meter = Meter(meter_location="huz.cab.err",
                                 manufacturer="Honeywell",
                                 measurement_frequency=5,
                                 measurement_unit=MeasurementUnit.LITERS_PER_SECOND,
                                 meter_type=MeterType.FLOW, measure_mode=MeterMeasureMode.AUTOMATIC)

        ups = UninterruptiblePowerSupply("UPS.01", PowerState.ON, UPSPhase.SINGLE)
        voltage_meter = Meter(meter_location="huz.cab.err",
                              manufacturer="Honeywell",
                              measurement_frequency=5,
                              measurement_unit=MeasurementUnit.VOLT,
                              meter_type=MeterType.POWER, measure_mode=MeterMeasureMode.AUTOMATIC)

        ups.meter = voltage_meter

        boiler = Boiler('PR.VNT.BL.01', BoilerCategory.NATURAL_GAS, PowerState.ON)
        boiler.meter = water_flow_meter

        mechanical_room = copy.copy(self.room)
        mechanical_room.room_type = RoomType.MECHANICAL
        self.room.add_energy_system(ups)
        mechanical_room.add_hvac_component(boiler)

        building.add_meter(electricity_meter)
        meter_types = [MeterType.FLOW.value, MeterType.ELECTRICITY.value, MeterType.POWER.value]
        meter_search = MeterSearchVisitor(
            floor_criteria={'number': [1, 2]},
            meter_criteria={'meter_type': meter_types})

        building.accept(meter_search)

        self.assertEqual(len(meter_search.found_entities), 3)
        self.assertEqual(meter_search.found_entities.count(water_flow_meter), 1)
        self.assertEqual(meter_search.found_entities.count(electricity_meter), 1)
        self.assertEqual(meter_search.found_entities.count(voltage_meter), 1)

    def test_search_meters_in_zones(self):
        self.hall.add_transducer(self.presence_sensor)
        self.hall.add_transducer(self.temp_sensor)
        second_floor = Floor(self.floor_area, 2, FloorType.ROOFTOP, rooms=[self.hall])
        building = Building(2009, self.height, self.floor_area, self.internal_mass, self.address,
                            BuildingType.RESIDENTIAL, [self.floor, second_floor])

        cooling_zone = Zone("HVAC_COOLING_ZONE", ZoneType.HVAC, HVACType.PERIMETER)
        heating_zone = Zone("HVAC_HEATING_ZONE", ZoneType.HVAC, HVACType.PERIMETER)

        electricity_meter = Meter(meter_location="huz.cab.err",
                                  manufacturer="Honeywell",
                                  measurement_frequency=5,
                                  measurement_unit=MeasurementUnit.KILOWATTS_PER_HOUR,
                                  meter_type=MeterType.ELECTRICITY, measure_mode=MeterMeasureMode.AUTOMATIC)

        water_flow_meter = Meter(meter_location="huz.cab.err",
                                 manufacturer="Honeywell",
                                 measurement_frequency=5,
                                 measurement_unit=MeasurementUnit.LITERS_PER_SECOND,
                                 meter_type=MeterType.FLOW, measure_mode=MeterMeasureMode.AUTOMATIC)

        ups = UninterruptiblePowerSupply("UPS.01", PowerState.ON, UPSPhase.SINGLE)
        voltage_meter = Meter(meter_location="huz.cab.err",
                              manufacturer="Honeywell",
                              measurement_frequency=5,
                              measurement_unit=MeasurementUnit.VOLT,
                              meter_type=MeterType.POWER, measure_mode=MeterMeasureMode.AUTOMATIC)

        ups.meter = voltage_meter

        boiler = Boiler('PR.VNT.BL.01', BoilerCategory.NATURAL_GAS, PowerState.ON)
        boiler.meter = water_flow_meter
        mechanical_room = copy.copy(self.room)
        mechanical_room.room_type = RoomType.MECHANICAL
        mechanical_room.add_hvac_component(boiler)
        self.room.add_energy_system(ups)

        self.room.add_zone(cooling_zone, building)
        mechanical_room.add_zone(heating_zone, building)

        building.add_meter(electricity_meter)
        meter_types = [MeterType.FLOW.value, MeterType.ELECTRICITY.value, MeterType.POWER.value]
        meter_search = MeterSearchVisitor(meter_criteria={'meter_type': meter_types},
                                          room_criteria={'zones': [cooling_zone]},
                                          open_space_criteria={'zones': [cooling_zone]})

        building.accept(meter_search)

        self.assertEqual(len(meter_search.found_entities), 3)
        self.assertEqual(meter_search.found_entities.count(water_flow_meter), 1)
        self.assertEqual(meter_search.found_entities.count(electricity_meter), 1)
        self.assertEqual(meter_search.found_entities.count(voltage_meter), 1)
