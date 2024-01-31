from unittest import TestCase
from misc import MeasureFactory
from enumerations import RecordingType
from datatypes.measure import Measure
from enumerations import MeasurementUnit
from structure.open_space import OpenSpace
from enumerations import OpenSpaceType
from enumerations import RoomType
from structure.room import Room
from structure.floor import Floor
from enumerations import FloorType
from datatypes.operational_schedule import OperationalSchedule
from datatypes.zone import Zone
from enumerations import ZoneType
from datetime import datetime
from datetime import timedelta


class TestFloor(TestCase):

    def setUp(self) -> None:
        self.area = MeasureFactory.create_measure(RecordingType.BINARY.value,
                                                  Measure(MeasurementUnit.SQUARE_METER, 45))
        self.room = Room(self.area, "Room 145", RoomType.BEDROOM)
        self.hall = OpenSpace("LECTURE_HALL_1", self.area, OpenSpaceType.HALL)

    def test_floor_with_no_room_and_open_space(self):
        try:
            Floor(self.area, 1, FloorType.REGULAR)
        except ValueError as err:
            self.assertEqual(err.__str__(), "A floor must have at least one room or one open space.")

    def test_floor_with_one_room_and_no_open_space(self):
        floor = Floor(area=self.area, number=1, floor_type=FloorType.REGULAR, rooms=[self.room])
        self.assertEqual(floor.rooms[0], self.room)
        self.assertEqual(len(floor.rooms), 1)
        self.assertEqual(len(floor.open_spaces), 0)

    def test_floor_with_one_room_and_one_open_space(self):
        floor = Floor(area=self.area, number=1, floor_type=FloorType.REGULAR,
                      rooms=[self.room], open_spaces=[self.hall])
        self.assertEqual(floor.rooms, [self.room])
        self.assertEqual(floor.open_spaces, [self.hall])
        self.assertEqual(floor.open_spaces[0].space_type, OpenSpaceType.HALL)

    def test_remove_room_from_floor(self):
        floor = Floor(area=self.area, number=1, floor_type=FloorType.REGULAR,
                      rooms=[self.room], open_spaces=[self.hall])
        self.assertEqual(floor.rooms[0], self.room)
        self.assertEqual(len(floor.rooms), 1)
        # Remove rooms
        floor.remove_room(self.room.UID)
        # Assert no rooms
        self.assertEqual(floor.rooms, [])

    def test_remove_open_space_from_floor(self):
        floor = Floor(area=self.area, number=1, floor_type=FloorType.REGULAR, open_spaces=[self.hall])
        self.assertEqual(floor.open_spaces[0], self.hall)
        # Remove open space
        floor.remove_open_space(self.hall.UID)
        # Assert no open space
        self.assertEqual(floor.open_spaces, [])

    def test_add_zone_to_floor(self):
        floor = Floor(area=self.area, number=1, floor_type=FloorType.REGULAR, open_spaces=[self.hall])
        hvac_zone = Zone('HVAC ZONE', ZoneType.HVAC)
        # Remove open space
        floor.add_zone(hvac_zone)
        # Assert no open space
        self.assertEqual(floor.zones, [hvac_zone])
        self.assertEqual(floor.zones[0].spaces, [floor])

    def test_add_floor_recurring_operational_schedule(self):
        schedule = OperationalSchedule("WEEKDAYS", datetime.now(), datetime.now() + timedelta(days=5))
        floor = Floor(area=self.area, number=1, floor_type=FloorType.REGULAR, open_spaces=[self.hall])
        floor.add_operational_schedule(schedule)
        self.assertEqual(floor.operational_schedule, [schedule])
        self.assertEqual(floor.operational_schedule[0].recurring, True)

    def test_add_floor_non_recurring_operational_schedule(self):
        schedule = OperationalSchedule("WEEKENDS", datetime.now(), datetime.now() + timedelta(days=2), recurring=False)
        floor = Floor(area=self.area, number=1, floor_type=FloorType.REGULAR, open_spaces=[self.hall])
        floor.add_operational_schedule(schedule)
        self.assertEqual(floor.operational_schedule, [schedule])
        self.assertEqual(floor.operational_schedule[0].recurring, False)

    def test_add_existing_schedule_to_floor(self):
        schedule = OperationalSchedule("WEEKENDS", datetime.now(), datetime.now() + timedelta(days=2), recurring=False)
        floor = Floor(area=self.area, number=1, floor_type=FloorType.REGULAR, open_spaces=[self.hall])
        floor.add_operational_schedule(schedule)
        floor.add_operational_schedule(schedule)
        self.assertEqual(floor.operational_schedule, [schedule])
        self.assertEqual(len(floor.operational_schedule), 1)







