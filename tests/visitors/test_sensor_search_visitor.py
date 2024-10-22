from metamenth.enumerations import OpenSpaceType
from metamenth.structure.floor import Floor
from metamenth.enumerations import FloorType
from metamenth.structure.building import Building
from metamenth.enumerations import BuildingType
from metamenth.virtual.zone import Zone
from metamenth.enumerations import ZoneType
from metamenth.enumerations import HVACType
from tests.structure.base_test import BaseTest
from metamenth.enumerations import RoomType
from metamenth.visitors.sensor_search_visitor import SensorSearchVisitor
from metamenth.enumerations import BoilerCategory
from metamenth.subsystem.hvac_components.boiler import Boiler
from metamenth.subsystem.appliance import Appliance
from metamenth.enumerations import ApplianceType
from metamenth.enumerations import ApplianceCategory
from metamenth.enumerations import MeasurementUnit
from metamenth.enumerations import PowerState
from metamenth.subsystem.hvac_components.heat_exchanger import HeatExchanger
from metamenth.enumerations import HeatExchangerType
from metamenth.enumerations import HeatExchangerFlowType
from metamenth.energysystem.solar_pv import SolarPV
from metamenth.enumerations import SolarPVType
from metamenth.enumerations import CellType
from metamenth.transducers.sensor import Sensor
from metamenth.enumerations import SensorMeasure
from metamenth.enumerations import SensorMeasureType
from metamenth.enumerations import SensorLogType
import copy


class TestSensorSearchVisitor(BaseTest):

    def test_search_room_and_open_space_sensors(self):
        self.hall.add_transducer(self.presence_sensor)
        self.room.add_transducer(self.temp_sensor)
        second_floor = Floor(self.floor_area, 2, FloorType.ROOFTOP, rooms=[self.hall])
        building = Building(2009, self.height, self.floor_area, self.internal_mass, self.address,
                            BuildingType.RESIDENTIAL, [self.floor, second_floor])

        sensor_search = SensorSearchVisitor(sensor_criteria={},
                                            room_criteria={'room_type': RoomType.BEDROOM.value},
                                            open_space_criteria={'space_type': OpenSpaceType.HALL.value})
        building.accept(sensor_search)
        self.assertEqual(len(sensor_search.found_entities), 2)
        self.assertEqual(sensor_search.found_entities[0].measure, SensorMeasure.TEMPERATURE)

    def test_search_space_sensor_with_floor_criteria(self):
        self.hall.add_transducer(self.presence_sensor)
        self.room.add_transducer(self.temp_sensor)
        second_floor = Floor(self.floor_area, 2, FloorType.ROOFTOP, rooms=[self.hall])
        building = Building(2009, self.height, self.floor_area, self.internal_mass, self.address,
                            BuildingType.RESIDENTIAL, [self.floor, second_floor])

        sensor_search = SensorSearchVisitor(sensor_criteria={},
                                            floor_criteria={'number': 1},
                                            room_criteria={'room_type': RoomType.BEDROOM.value},
                                            open_space_criteria={'space_type': OpenSpaceType.HALL.value})
        building.accept(sensor_search)
        self.assertEqual(len(sensor_search.found_entities), 1)
        self.assertEqual(sensor_search.found_entities[0], self.temp_sensor)

    def test_search_space_and_hvac_component_sensors(self):
        self.hall.add_transducer(self.presence_sensor)
        self.room.add_transducer(self.temp_sensor)
        second_floor = Floor(self.floor_area, 2, FloorType.ROOFTOP, rooms=[self.hall])
        building = Building(2009, self.height, self.floor_area, self.internal_mass, self.address,
                            BuildingType.RESIDENTIAL, [self.floor, second_floor])

        boiler = Boiler('PR.VNT.BL.01', BoilerCategory.NATURAL_GAS, PowerState.ON)
        boiler.add_transducer(self.temp_sensor)

        heat_exchanger = HeatExchanger("PR.VNT.HE.01", HeatExchangerType.FIN_TUBE, HeatExchangerFlowType.PARALLEL)
        heat_exchanger.add_transducer(self.temp_sensor)

        mechanical_room = copy.copy(self.room)
        mechanical_room.room_type = RoomType.MECHANICAL
        mechanical_room.add_hvac_component(boiler)
        mechanical_room.add_hvac_component(heat_exchanger)

        sensor_search = SensorSearchVisitor(sensor_criteria={
            'measure': [SensorMeasure.TEMPERATURE.value, SensorMeasure.OCCUPANCY.value],
        },
            floor_criteria={'number': [1, 2]})
        building.accept(sensor_search)

        self.assertEqual(len(sensor_search.found_entities), 4)
        self.assertIn(self.presence_sensor, sensor_search.found_entities)
        self.assertEqual(sensor_search.found_entities.count(self.temp_sensor), 3)

    def test_search_space_hvac_component_and_appliance_sensors(self):
        self.hall.add_transducer(self.presence_sensor)
        self.room.add_transducer(self.temp_sensor)
        second_floor = Floor(self.floor_area, 2, FloorType.ROOFTOP, rooms=[self.hall])
        building = Building(2009, self.height, self.floor_area, self.internal_mass, self.address,
                            BuildingType.RESIDENTIAL, [self.floor, second_floor])

        boiler = Boiler('PR.VNT.BL.01', BoilerCategory.NATURAL_GAS, PowerState.ON)
        boiler.add_transducer(self.temp_sensor)

        heat_exchanger = HeatExchanger("PR.VNT.HE.01", HeatExchangerType.FIN_TUBE, HeatExchangerFlowType.PARALLEL)
        heat_exchanger.add_transducer(self.temp_sensor)

        mechanical_room = copy.copy(self.room)
        mechanical_room.room_type = RoomType.MECHANICAL
        mechanical_room.add_hvac_component(boiler)
        mechanical_room.add_hvac_component(heat_exchanger)

        smart_camera = Appliance("Smart Camera", [ApplianceCategory.OFFICE, ApplianceCategory.SMART],
                                 ApplianceType.CAMERA)
        smart_camera.add_transducer(self.presence_sensor)
        self.room.add_appliance(smart_camera)

        sensor_search = SensorSearchVisitor(sensor_criteria={},
                                            floor_criteria={'number': 1})
        building.accept(sensor_search)

        self.assertEqual(len(sensor_search.found_entities), 4)
        self.assertIn(self.temp_sensor, sensor_search.found_entities)
        self.assertEqual(sensor_search.found_entities.count(self.presence_sensor), 1)
        self.assertEqual(sensor_search.found_entities.count(self.temp_sensor), 3)

    def test_search_space_hvac_component_appliance_and_energy_system_sensors(self):
        self.hall.add_transducer(self.presence_sensor)
        self.room.add_transducer(self.temp_sensor)
        second_floor = Floor(self.floor_area, 2, FloorType.ROOFTOP, rooms=[self.hall])
        building = Building(2009, self.height, self.floor_area, self.internal_mass, self.address,
                            BuildingType.RESIDENTIAL, [self.floor, second_floor])

        boiler = Boiler('PR.VNT.BL.01', BoilerCategory.NATURAL_GAS, PowerState.ON)
        boiler.add_transducer(self.temp_sensor)

        heat_exchanger = HeatExchanger("PR.VNT.HE.01", HeatExchangerType.FIN_TUBE, HeatExchangerFlowType.PARALLEL)
        heat_exchanger.add_transducer(self.temp_sensor)

        mechanical_room = copy.copy(self.room)
        mechanical_room.add_transducer(self.temp_sensor)
        mechanical_room.room_type = RoomType.MECHANICAL
        mechanical_room.add_hvac_component(boiler)
        mechanical_room.add_hvac_component(heat_exchanger)

        smart_camera = Appliance("Smart Camera", [ApplianceCategory.OFFICE, ApplianceCategory.SMART],
                                 ApplianceType.CAMERA)
        smart_camera.add_transducer(self.presence_sensor)
        self.room.add_appliance(smart_camera)

        solar_pv = SolarPV("Solar Panels", False, MeasurementUnit.WATTS,
                           SolarPVType.BUILDING_INTEGRATED_PHOTOVOLTAIC, CellType.AMORPHOUS)

        temp_sensor = Sensor("PV.TEMPERATURE.SENSOR", SensorMeasure.TEMPERATURE, MeasurementUnit.DEGREE_CELSIUS,
                             SensorMeasureType.THERMO_COUPLE_TYPE_A, 900, sensor_log_type=SensorLogType.POLLING)
        voltage_sensor = Sensor("PV.VOLTAGE.SENSOR", SensorMeasure.VOLTAGE, MeasurementUnit.VOLT,
                                SensorMeasureType.THERMO_COUPLE_TYPE_A, 900, sensor_log_type=SensorLogType.POLLING)
        solar_pv.add_transducer(temp_sensor)
        solar_pv.add_transducer(voltage_sensor)

        self.hall.add_energy_system(solar_pv)

        sensor_search = SensorSearchVisitor(sensor_criteria={'data_frequency': 900},
                                            floor_criteria={'number': 2})
        building.accept(sensor_search)
        self.assertEqual(len(sensor_search.found_entities), 2)
        self.assertIn(temp_sensor, sensor_search.found_entities)
        self.assertEqual(sensor_search.found_entities.count(voltage_sensor), 1)
        self.assertEqual(sensor_search.found_entities.count(self.temp_sensor), 0)

    def test_search_sensors_with_unmatched_criteria(self):
        self.hall.add_transducer(self.presence_sensor)
        self.room.add_transducer(self.temp_sensor)
        second_floor = Floor(self.floor_area, 2, FloorType.ROOFTOP, rooms=[self.hall])
        building = Building(2009, self.height, self.floor_area, self.internal_mass, self.address,
                            BuildingType.RESIDENTIAL, [self.floor, second_floor])
        boiler = Boiler('PR.VNT.BL.01', BoilerCategory.NATURAL_GAS, PowerState.ON)
        boiler.add_transducer(self.temp_sensor)

        heat_exchanger = HeatExchanger("PR.VNT.HE.01", HeatExchangerType.FIN_TUBE, HeatExchangerFlowType.PARALLEL)
        heat_exchanger.add_transducer(self.temp_sensor)

        mechanical_room = copy.copy(self.room)
        mechanical_room.room_type = RoomType.MECHANICAL
        mechanical_room.add_hvac_component(boiler)
        mechanical_room.add_hvac_component(heat_exchanger)

        sensor_search = SensorSearchVisitor(floor_criteria={'number': 3}, sensor_criteria={})
        building.accept(sensor_search)
        self.assertEqual(len(sensor_search.found_entities), 0)

    def test_search_zonal_sensors(self):
        self.hall.add_transducer(self.presence_sensor)
        self.room.add_transducer(self.temp_sensor)
        second_floor = Floor(self.floor_area, 2, FloorType.ROOFTOP, rooms=[self.hall])
        building = Building(2009, self.height, self.floor_area, self.internal_mass, self.address,
                            BuildingType.RESIDENTIAL, [self.floor, second_floor])

        cooling_zone = Zone("HVAC_COOLING_ZONE", ZoneType.HVAC, HVACType.PERIMETER)
        heating_zone = Zone("HVAC_HEATING_ZONE", ZoneType.HVAC, HVACType.PERIMETER)

        building.get_floor_by_uid(self.floor.UID).add_zone(cooling_zone, building)
        building.get_floor_by_uid(second_floor.UID).add_zone(heating_zone, building)

        sensor_search = SensorSearchVisitor(sensor_criteria={},  floor_criteria={'zones': [cooling_zone]})

        building.accept(sensor_search)
        self.assertEqual(len(sensor_search.found_entities), 1)
        self.assertIn(self.temp_sensor, sensor_search.found_entities)
        self.assertNotIn(self.presence_sensor, sensor_search.found_entities)
