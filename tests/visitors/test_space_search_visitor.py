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
from metamenth.visitors.space_search_visitor import SpaceSearchVisitor
from metamenth.enumerations import MeasurementUnit
from metamenth.misc import MeasureFactory
from metamenth.enumerations import RecordingType
from metamenth.datatypes.measure import Measure
from metamenth.structure.room import Room
from metamenth.structure.open_space import OpenSpace


class TestSpaceSearchVisitor(BaseTest):

    def test_search_specific_floor_types(self):
        second_floor = Floor(self.floor_area, 2, FloorType.ROOFTOP, rooms=[self.room])
        building = Building(2009, self.height, self.floor_area, self.internal_mass, self.address,
                            BuildingType.RESIDENTIAL, [self.floor, second_floor])

        space_search = SpaceSearchVisitor(floor_criteria={'floor_type': FloorType.ROOFTOP.value})
        building.accept(space_search)

        self.assertEqual(len(space_search.found_entities), 2)
        self.assertEqual(space_search.found_entities.count(second_floor), 1)
        self.assertEqual(space_search.found_entities.count(self.room), 1)
        self.assertEqual(space_search.found_entities.count(self.floor), 0)
        self.assertEqual(space_search.found_entities.count(self.hall), 0)

    def test_search_specific_floor_types_with_multiple_conditions(self):
        second_floor = Floor(self.floor_area, 2, FloorType.ROOFTOP, open_spaces=[self.hall])
        building = Building(2009, self.height, self.floor_area, self.internal_mass, self.address,
                            BuildingType.RESIDENTIAL, [self.floor, second_floor])

        space_search = SpaceSearchVisitor(floor_criteria={'floor_type': FloorType.REGULAR.value,
                                                          'area': self.area})
        building.accept(space_search)

        self.assertEqual(len(space_search.found_entities), 2)
        self.assertEqual(space_search.found_entities.count(second_floor), 0)
        self.assertEqual(space_search.found_entities.count(self.room), 1)
        self.assertEqual(space_search.found_entities.count(self.floor), 1)
        self.assertEqual(space_search.found_entities.count(self.hall), 0)

    def test_search_floors_with_unmatched_criteria(self):
        second_floor = Floor(self.floor_area, 2, FloorType.ROOFTOP, open_spaces=[self.hall])
        building = Building(2009, self.height, self.floor_area, self.internal_mass, self.address,
                            BuildingType.RESIDENTIAL, [self.floor, second_floor])

        space_search = SpaceSearchVisitor(floor_criteria={'floor_type': FloorType.BASEMENT.value,
                                                          'area': self.floor_area})
        building.accept(space_search)

        self.assertEqual(len(space_search.found_entities), 0)

    def test_search_floor_in_hvac_zone(self):
        self.hall.add_transducer(self.presence_sensor)
        self.room.add_transducer(self.temp_sensor)
        second_floor = Floor(self.floor_area, 2, FloorType.ROOFTOP, open_spaces=[self.hall])
        building = Building(2009, self.height, self.floor_area, self.internal_mass, self.address,
                            BuildingType.RESIDENTIAL, [self.floor, second_floor])

        cooling_zone = Zone("HVAC_COOLING_ZONE", ZoneType.HVAC, HVACType.PERIMETER)
        heating_zone = Zone("HVAC_HEATING_ZONE", ZoneType.HVAC, HVACType.PERIMETER)

        self.floor.add_zone(cooling_zone, building)
        second_floor.add_zone(heating_zone, building)

        space_search = SpaceSearchVisitor(floor_criteria={'zones': [heating_zone]})
        building.accept(space_search)

        self.assertEqual(len(space_search.found_entities), 2)
        self.assertEqual(space_search.found_entities.count(second_floor), 1)
        self.assertEqual(space_search.found_entities.count(self.room), 0)
        self.assertEqual(space_search.found_entities.count(self.floor), 0)
        self.assertEqual(space_search.found_entities.count(self.hall), 1)

    def test_search_rooms_and_open_spaces_of_same_size(self):
        second_floor = Floor(self.floor_area, 2, FloorType.ROOFTOP, open_spaces=[self.hall])
        building = Building(2009, self.height, self.floor_area, self.internal_mass, self.address,
                            BuildingType.RESIDENTIAL, [self.floor, second_floor])

        area = MeasureFactory.create_measure(RecordingType.BINARY.value,
                                             Measure(MeasurementUnit.SQUARE_METERS, 45))
        office = Room(self.area, "Office 200", RoomType.OFFICE)
        corridor = OpenSpace("Corridor 100", area, OpenSpaceType.CORRIDOR)

        second_floor.add_rooms([office])
        self.floor.add_open_spaces([corridor])

        space_search = SpaceSearchVisitor(room_criteria={'area': self.area}, open_space_criteria={'area': area},
                                          include_floor=False)
        building.accept(space_search)

        self.assertEqual(len(space_search.found_entities), 3)
        self.assertEqual(space_search.found_entities.count(office), 1)
        self.assertEqual(space_search.found_entities.count(corridor), 1)
        self.assertEqual(space_search.found_entities.count(self.room), 1)
        self.assertEqual(space_search.found_entities.count(self.hall), 0)

    def test_search_rooms_and_open_spaces_on_floor(self):
        second_floor = Floor(self.floor_area, 2, FloorType.ROOFTOP, open_spaces=[self.hall])
        building = Building(2009, self.height, self.floor_area, self.internal_mass, self.address,
                            BuildingType.RESIDENTIAL, [self.floor, second_floor])

        area = MeasureFactory.create_measure(RecordingType.BINARY.value,
                                             Measure(MeasurementUnit.SQUARE_METERS, 45))
        office = Room(self.area, "Office 200", RoomType.OFFICE)
        corridor = OpenSpace("Corridor 100", area, OpenSpaceType.CORRIDOR)

        second_floor.add_rooms([office])
        self.floor.add_open_spaces([corridor])

        space_search = SpaceSearchVisitor(floor_criteria={'number': 1}, include_floor=False)
        building.accept(space_search)

        self.assertEqual(len(space_search.found_entities), 2)
        self.assertEqual(space_search.found_entities.count(office), 0)
        self.assertEqual(space_search.found_entities.count(corridor), 1)
        self.assertEqual(space_search.found_entities.count(self.room), 1)
        self.assertEqual(space_search.found_entities.count(self.hall), 0)
