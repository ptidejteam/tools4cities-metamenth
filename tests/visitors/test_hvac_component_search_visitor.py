from structure.floor import Floor
from enumerations import FloorType
from virtual.zone import Zone
from enumerations import ZoneType
from enumerations import HVACType
from enumerations import RoomType
from enumerations import PowerState
from subsystem.hvac_components.heat_exchanger import HeatExchanger
from enumerations import HeatExchangerType
from enumerations import HeatExchangerFlowType
from subsystem.hvac_components.damper import Damper
from enumerations import DamperType
from tests.subsystem.base_test import BaseTest
from subsystem.hvac_components.boiler import Boiler
from enumerations import BoilerCategory
from subsystem.hvac_components.air_volume_box import AirVolumeBox
from enumerations import AirVolumeType
from visitors.hvac_component_search_visitor import HVACComponentSearchVisitor
from subsystem.hvac_components.duct import Duct
from enumerations import DuctType
from enumerations import DuctSubType


class TestHVACComponentSearchVisitor(BaseTest):

    def test_search_hvac_component_without_component_class(self):
        room_vav_box = AirVolumeBox('PR.VNT.VAV.01', AirVolumeType.VARIABLE_AIR_VOLUME)
        hall_vav_box = AirVolumeBox('PR.VNT.VAV.02', AirVolumeType.CONSTANT_AIR_VOLUME)

        second_floor = Floor(self.floor_area, 2, FloorType.ROOFTOP, open_spaces=[self.hall])

        self.building.add_floors([second_floor])
        self.room.add_hvac_component(room_vav_box)
        self.hall.add_hvac_component(hall_vav_box)

        try:
            hvac_search = HVACComponentSearchVisitor(hvac_component_criteria={'has_heating_capacity': True})
            self.building.accept(hvac_search)
        except ValueError as err:
            self.assertEqual(err.__str__(),
                             "hvac component criteria must have component_class value: {'has_heating_capacity': True}")

    def test_search_hvac_component_with_non_existent_component_class(self):
        room_vav_box = AirVolumeBox('PR.VNT.VAV.01', AirVolumeType.VARIABLE_AIR_VOLUME)
        hall_vav_box = AirVolumeBox('PR.VNT.VAV.02', AirVolumeType.CONSTANT_AIR_VOLUME)

        second_floor = Floor(self.floor_area, 2, FloorType.ROOFTOP, open_spaces=[self.hall])

        self.building.add_floors([second_floor])
        self.room.add_hvac_component(room_vav_box)
        self.hall.add_hvac_component(hall_vav_box)

        hvac_search = HVACComponentSearchVisitor(hvac_component_criteria={'component_class': 'Coil',
                                                                          'has_heating_capacity': True})
        self.building.accept(hvac_search)
        self.assertEqual(len(hvac_search.found_entities), 0)

    def test_search_hvac_component_with_unmatched_component_class_attributes(self):
        room_vav_box = AirVolumeBox('PR.VNT.VAV.01', AirVolumeType.VARIABLE_AIR_VOLUME)
        hall_vav_box = AirVolumeBox('PR.VNT.VAV.02', AirVolumeType.CONSTANT_AIR_VOLUME)
        room_damper = Damper('PR.VNT.DMP.01', DamperType.MANUAL_VOLUME)
        room_vav_box.inlet_dampers = [room_damper]
        hall_damper = Damper('PR.VNT.DMP.02', DamperType.BASIC_MANUAL_VOLUME)
        hall_vav_box.inlet_dampers = [hall_damper]
        second_floor = Floor(self.floor_area, 2, FloorType.ROOFTOP, open_spaces=[self.hall])

        self.building.add_floors([second_floor])
        self.room.add_hvac_component(room_vav_box)
        self.hall.add_hvac_component(hall_vav_box)

        hvac_search = HVACComponentSearchVisitor(hvac_component_criteria={'component_class': 'AirVolumeBox',
                                                                          'damper_type': DamperType.MANUAL_VOLUME.value})
        self.building.accept(hvac_search)
        self.assertEqual(len(hvac_search.found_entities), 0)

    def test_search_dampers_in_specific_zones(self):
        room_vav_box = AirVolumeBox('PR.VNT.VAV.01', AirVolumeType.VARIABLE_AIR_VOLUME)
        hall_vav_box = AirVolumeBox('PR.VNT.VAV.02', AirVolumeType.CONSTANT_AIR_VOLUME)
        room_damper = Damper('PR.VNT.DMP.01', DamperType.MANUAL_VOLUME)
        room_vav_box.inlet_dampers = [room_damper]
        hall_damper = Damper('PR.VNT.DMP.02', DamperType.BASIC_MANUAL_VOLUME)
        hall_vav_box.inlet_dampers = [hall_damper]
        second_floor = Floor(self.floor_area, 2, FloorType.ROOFTOP, open_spaces=[self.hall])

        self.building.add_floors([second_floor])
        self.room.add_hvac_component(room_vav_box)
        self.hall.add_hvac_component(hall_vav_box)

        cooling_zone = Zone("HVAC_COOLING_ZONE", ZoneType.HVAC, HVACType.PERIMETER)
        heating_zone = Zone("HVAC_HEATING_ZONE", ZoneType.HVAC, HVACType.PERIMETER)

        self.floor.add_zone(cooling_zone, self.building)
        second_floor.add_zone(heating_zone, self.building)

        hvac_search = HVACComponentSearchVisitor(hvac_component_criteria={'component_class': 'Damper',
                                                                          'damper_type': DamperType.MANUAL_VOLUME.value},
                                                 floor_criteria={'zones': [cooling_zone]})

        self.building.accept(hvac_search)

        self.assertEqual(len(hvac_search.found_entities), 1)
        self.assertIn(room_damper, hvac_search.found_entities)
        self.assertNotIn(hall_damper, hvac_search.found_entities)

    def test_search_for_all_vav_boxes(self):
        room_vav_box = AirVolumeBox('PR.VNT.VAV.01', AirVolumeType.VARIABLE_AIR_VOLUME)
        hall_vav_box = AirVolumeBox('PR.VNT.VAV.02', AirVolumeType.CONSTANT_AIR_VOLUME)
        room_damper = Damper('PR.VNT.DMP.01', DamperType.MANUAL_VOLUME)
        room_vav_box.inlet_dampers = [room_damper]
        hall_damper = Damper('PR.VNT.DMP.02', DamperType.BASIC_MANUAL_VOLUME)
        hall_vav_box.inlet_dampers = [hall_damper]
        second_floor = Floor(self.floor_area, 2, FloorType.ROOFTOP, open_spaces=[self.hall])

        self.building.add_floors([second_floor])
        self.room.add_hvac_component(room_vav_box)
        self.hall.add_hvac_component(hall_vav_box)

        hvac_search = HVACComponentSearchVisitor(hvac_component_criteria={'component_class': 'AirVolumeBox'},
                                                 floor_criteria={'number': [1, 2]})

        self.building.accept(hvac_search)

        self.assertEqual(len(hvac_search.found_entities), 2)
        self.assertIn(room_vav_box, hvac_search.found_entities)
        self.assertIn(hall_vav_box, hvac_search.found_entities)
        self.assertNotIn(room_damper, hvac_search.found_entities)
        self.assertNotIn(hall_damper, hvac_search.found_entities)

    def test_search_for_room_and_duct_dampers(self):
        room_damper = Damper('PR.VNT.DMP.01', DamperType.MANUAL_VOLUME)
        duct_damper = Damper('PR.VNT.DMP.02', DamperType.BIOMETRIC_BYPASS)
        room_damper.percentage_opened = 70
        duct_damper.percentage_opened = 70
        second_floor = Floor(self.floor_area, 2, FloorType.ROOFTOP, open_spaces=[self.hall])
        self.building.add_floors([second_floor])

        supply_air_duct = Duct("SUPP.VNT.01", DuctType.AIR)
        supply_air_duct.duct_sub_type = DuctSubType.FRESH_AIR
        supply_air_duct.add_damper(duct_damper)

        self.room.add_hvac_component(room_damper)
        self.hall.add_hvac_component(supply_air_duct)

        hvac_search = HVACComponentSearchVisitor(hvac_component_criteria={'component_class': 'Damper',
                                                                          'percentage_opened': 70})
        self.building.accept(hvac_search)

        self.assertEqual(len(hvac_search.found_entities), 2)
        self.assertIn(duct_damper, hvac_search.found_entities)
        self.assertIn(room_damper, hvac_search.found_entities)

    def test_search_for_heat_exchangers_in_ducts(self):
        room_damper = Damper('PR.VNT.DMP.01', DamperType.MANUAL_VOLUME)
        duct_damper = Damper('PR.VNT.DMP.02', DamperType.BIOMETRIC_BYPASS)
        room_damper.percentage_opened = 70
        duct_damper.percentage_opened = 70
        second_floor = Floor(self.floor_area, 2, FloorType.ROOFTOP, open_spaces=[self.hall])
        self.building.add_floors([second_floor])

        supply_air_duct = Duct("SUPP.VNT.01", DuctType.AIR)
        supply_air_duct.duct_sub_type = DuctSubType.FRESH_AIR
        supply_air_duct.add_damper(duct_damper)

        heat_exchanger_one = HeatExchanger("PR.VNT.HE.01", HeatExchangerType.FIN_TUBE, HeatExchangerFlowType.PARALLEL)
        heat_exchanger_two = HeatExchanger("PR.VNT.HE.02", HeatExchangerType.PLATED_FIN, HeatExchangerFlowType.PARALLEL)
        supply_air_duct.add_heat_exchanger(heat_exchanger_one)
        supply_air_duct.add_heat_exchanger(heat_exchanger_two)

        return_air_duct = Duct("SUPP.VNT.01", DuctType.AIR)
        return_air_duct.duct_sub_type = DuctSubType.RETURN_AIR

        self.room.add_hvac_component(room_damper)
        self.hall.add_hvac_component(supply_air_duct)
        self.room.add_hvac_component(return_air_duct)

        hvac_search = HVACComponentSearchVisitor(hvac_component_criteria={
            'component_class': 'HeatExchanger',
            'heat_exchanger_type': HeatExchangerType.PLATED_FIN.value},
            room_criteria={'room_type': RoomType.CAFETERIA.value})

        self.building.accept(hvac_search)

        self.assertEqual(len(hvac_search.found_entities), 1)
        self.assertIn(heat_exchanger_two, hvac_search.found_entities)
        self.assertNotIn(heat_exchanger_one, hvac_search.found_entities)

    def test_search_for_turned_on_boilers(self):
        second_floor = Floor(self.floor_area, 2, FloorType.ROOFTOP, open_spaces=[self.hall])
        self.building.add_floors([second_floor])
        self.room.room_type = RoomType.MECHANICAL

        boiler_one = Boiler('PR.VNT.BL.01', BoilerCategory.NATURAL_GAS, PowerState.ON)
        boiler_two = Boiler('PR.VNT.BL.02', BoilerCategory.BIOMASS, PowerState.OFF)

        self.room.add_hvac_component(boiler_one)
        self.room.add_hvac_component(boiler_two)

        hvac_search = HVACComponentSearchVisitor(hvac_component_criteria={
            'component_class': 'Boiler',
            'power_state': PowerState.ON.value},
            room_criteria={'room_type': RoomType.MECHANICAL.value})

        self.building.accept(hvac_search)
        self.assertEqual(len(hvac_search.found_entities), 1)
        self.assertEqual(hvac_search.found_entities.count(boiler_one), 1)
        self.assertEqual(hvac_search.found_entities.count(boiler_two), 0)
