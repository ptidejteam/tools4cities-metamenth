from unittest import TestCase
from misc import MeasureFactory
from enumerations import RecordingType
from datatypes.measure import Measure
from enumerations import MeasurementUnit
from structure.open_space import OpenSpace
from enumerations import OpenSpaceType
from enumerations import RoomType
from structure.room import Room
from virtual.zone import Zone
from enumerations import ZoneType
from enumerations import HVACType
from structure.floor import Floor
from enumerations import FloorType


class TestZone(TestCase):

    def setUp(self) -> None:
        self.area = MeasureFactory.create_measure(RecordingType.BINARY.value,
                                                  Measure(MeasurementUnit.SQUARE_METERS, 30))

    def test_hvac_zone_with_no_sub_zone(self):
       zone = Zone("COLD_ZONE", ZoneType.HVAC)
       self.assertIsNotNone(zone.UID)
       self.assertEqual(zone.name, "COLD_ZONE")
       self.assertEqual(zone.hvac_type, HVACType.NONE)

    def test_interior_hvac_zone(self):
        zone = Zone("WARM_ZONE", ZoneType.HVAC, HVACType.INTERIOR)
        self.assertIsNotNone(zone.UID)
        self.assertEqual(zone.zone_type, ZoneType.HVAC)
        self.assertEqual(zone.hvac_type, HVACType.INTERIOR)

    def test_lighting_zone(self):
        zone = Zone("DIM_ZONE", ZoneType.LIGHTING)
        self.assertIsNotNone(zone.UID)
        self.assertEqual(zone.zone_type, ZoneType.LIGHTING)
        self.assertEqual(zone.hvac_type, HVACType.NONE.value)

    def test_lighting_zone_with_hvac_type(self):
        zone = Zone("BRIGHT_ZONE", ZoneType.LIGHTING, HVACType.PERIMETER)
        self.assertEqual(zone.description, None)
        # a lighting zone cannot have an hvac type
        self.assertEqual(zone.hvac_type, HVACType.NONE.value)

    def test_zone_with_adjacent_zones(self):
        zone_1 = Zone(name="DIM_ZONE", zone_type=ZoneType.LIGHTING, description="Relaxation zone")
        zone_2 = Zone(name="WARM_ZONE", zone_type=ZoneType.HVAC, hvac_type=HVACType.INTERIOR, description="Heated Zone")
        zone_3 = Zone(name="COLD_ZONE", zone_type=ZoneType.HVAC, description="Data center area")
        zone_1.add_adjacent_zones([zone_2, zone_3])
        zone_2.add_adjacent_zones([zone_1, zone_3])
        self.assertEqual(zone_1.get_adjacent_zone_by_name("WARM_ZONE"), zone_2)
        self.assertEqual(zone_1.get_adjacent_zone_by_name("COLD_ZONE"), zone_3)
        self.assertEqual(zone_2.get_adjacent_zone_by_name("DIM_ZONE"), zone_1)
        self.assertEqual(zone_2.get_adjacent_zone_by_name("COLD_ZONE"), zone_3)
        self.assertEqual(zone_3.get_adjacent_zones(), [])

    def test_zone_with_overlapping_zones(self):
        zone_1 = Zone(name="DIM_ZONE", zone_type=ZoneType.LIGHTING, description="Relaxation zone")
        zone_2 = Zone(name="WARM_ZONE", zone_type=ZoneType.HVAC, hvac_type=HVACType.INTERIOR, description="Heated Zone")
        zone_3 = Zone(name="COLD_ZONE", zone_type=ZoneType.HVAC, description="Data center area")
        zone_1.add_overlapping_zones([zone_2, zone_3])
        zone_2.add_overlapping_zones([zone_1, zone_3])
        self.assertEqual(zone_1.get_overlapping_zone_by_name("WARM_ZONE"), zone_2)
        self.assertEqual(zone_1.get_overlapping_zone_by_name("COLD_ZONE"), zone_3)
        self.assertEqual(zone_2.get_overlapping_zone_by_name("DIM_ZONE"), zone_1)
        self.assertEqual(zone_2.get_overlapping_zone_by_name("COLD_ZONE"), zone_3)
        self.assertEqual(zone_3.get_overlapping_zones(), [])

    def test_zone_with_existing_adjacent_zone(self):
        zone = Zone(name="DIM_ZONE", zone_type=ZoneType.LIGHTING, description="Relaxation zone")
        adjacent_zone = Zone(name="COLD_ZONE", zone_type=ZoneType.HVAC, description="Data center area")
        zone.add_adjacent_zones([adjacent_zone])
        zone.add_adjacent_zones([adjacent_zone])
        # should not add a zone if there is an existing one with the same name. No duplicates
        self.assertEqual(zone.get_adjacent_zones(), [adjacent_zone])
        self.assertEqual(len(zone.get_adjacent_zones()), 1)

    def test_zone_with_room(self):
        zone = Zone("COLD_ZONE", ZoneType.HVAC)
        room = Room(self.area, "Room 145", RoomType.CLASSROOM)
        zone.add_spaces([room])
        self.assertEqual(len(zone.get_spaces()), 1)
        self.assertEqual(zone.get_space_by_uid(room.UID), room)

    def test_zone_with_room_and_open_space(self):
        zone = Zone("COLD_ZONE", ZoneType.HVAC)
        room = Room(self.area, "Room 145", RoomType.CLASSROOM)
        corridor = OpenSpace("CORRIDOR_3", self.area, OpenSpaceType.CORRIDOR)
        zone.add_spaces([room, corridor])
        self.assertEqual(len(zone.get_spaces()), 2)
        self.assertEqual(zone.get_space_by_uid(room.UID), room)
        self.assertEqual(zone.get_space_by_uid(corridor.UID), corridor)

    def test_zone_with_floor_and_spaces(self):
        zone = Zone("COLD_ZONE", ZoneType.HVAC)
        room = Room(self.area, "Room 145", RoomType.CLASSROOM)
        corridor = OpenSpace("CORRIDOR_2", self.area, OpenSpaceType.CORRIDOR)
        floor = Floor(area=self.area, number=1, floor_type=FloorType.REGULAR, rooms=[room], open_spaces=[corridor])
        zone.add_spaces([floor])
        self.assertEqual(len(zone.get_spaces()), 1)
        self.assertEqual(zone.get_space_by_uid(floor.UID), floor)
        self.assertEqual(zone.get_space_by_uid(floor.UID).floor_type, FloorType.REGULAR)

    def test_remove_adjacent_zone(self):
        zone = Zone(name="DIM_ZONE", zone_type=ZoneType.LIGHTING, description="Relaxation zone")
        adjacent_zone = Zone(name="COLD_ZONE", zone_type=ZoneType.HVAC, description="Data center area")
        zone.add_adjacent_zones([adjacent_zone])
        self.assertEqual(len(zone.get_adjacent_zones()), 1)
        zone.remove_adjacent_zone(adjacent_zone)
        self.assertEqual(len(zone.get_adjacent_zones()), 0)
        self.assertEqual(zone.get_adjacent_zones(), [])

    def test_remove_overlapping_zone(self):
        zone = Zone(name="DIM_ZONE", zone_type=ZoneType.LIGHTING, description="Relaxation zone")
        over_zone = Zone(name="COLD_ZONE", zone_type=ZoneType.HVAC, description="Data center area")
        zone.add_overlapping_zones([over_zone])

        self.assertEqual(len(zone.get_overlapping_zones()), 1)
        zone.remove_overlapping_zone(over_zone)
        self.assertEqual(len(zone.get_overlapping_zones()), 0)
        self.assertEqual(zone.get_overlapping_zones(), [])

    def test_remove_space_from_zone(self):
        zone = Zone("COLD_ZONE", ZoneType.HVAC)
        room = Room(self.area, "Room 145", RoomType.CLASSROOM)
        corridor = OpenSpace("CORRIDOR_1", self.area, OpenSpaceType.CORRIDOR)
        floor = Floor(area=self.area, number=1, floor_type=FloorType.REGULAR, rooms=[room], open_spaces=[corridor])
        zone.add_spaces([floor, corridor])
        self.assertEqual(len(zone.get_spaces()), 2)
        zone.remove_space(floor)
        self.assertEqual(zone.get_spaces(), [corridor])
        self.assertEqual(len(zone.get_spaces()), 1)





