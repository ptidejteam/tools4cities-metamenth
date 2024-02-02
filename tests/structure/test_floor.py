from enumerations import OpenSpaceType
from structure.floor import Floor
from enumerations import FloorType
from datatypes.operational_schedule import OperationalSchedule
from datetime import datetime
from datetime import timedelta
from .base_test import BaseTest


class TestFloor(BaseTest):

    def test_floor_with_no_room_and_open_space(self):
        try:
            Floor(self.area, 1, FloorType.REGULAR)
        except ValueError as err:
            self.assertEqual(err.__str__(), "A floor must have at least one room or one open space.")

    def test_floor_with_one_room_and_no_open_space(self):
        self.assertEqual(self.floor.rooms[0], self.room)
        self.assertEqual(len(self.floor.rooms), 1)
        self.assertEqual(len(self.floor.open_spaces), 0)

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
        floor.remove_room(self.room)
        # Assert no rooms
        self.assertEqual(floor.rooms, [])

    def test_remove_open_space_from_floor(self):
        floor = Floor(area=self.area, number=1, floor_type=FloorType.REGULAR, open_spaces=[self.hall])
        self.assertEqual(floor.open_spaces[0], self.hall)
        # Remove open space
        floor.remove_open_space(self.hall)
        # Assert no open space
        self.assertEqual(floor.open_spaces, [])

    def test_add_floor_recurring_operational_schedule(self):
        schedule = OperationalSchedule("WEEKDAYS", datetime.now(), datetime.now() + timedelta(days=5))
        floor = Floor(area=self.area, number=1, floor_type=FloorType.REGULAR, open_spaces=[self.hall])
        floor.add_schedule(schedule)
        self.assertEqual(floor.schedules, [schedule])
        self.assertEqual(floor.schedules[0].recurring, True)

    def test_add_floor_non_recurring_operational_schedule(self):
        schedule = OperationalSchedule("WEEKENDS", datetime.now(), datetime.now() + timedelta(days=2), recurring=False)
        floor = Floor(area=self.area, number=1, floor_type=FloorType.REGULAR, open_spaces=[self.hall])
        floor.add_schedule(schedule)
        self.assertEqual(floor.schedules, [schedule])
        self.assertEqual(floor.schedules[0].recurring, False)

    def test_add_existing_schedule_to_floor(self):
        schedule = OperationalSchedule("WEEKENDS", datetime.now(), datetime.now() + timedelta(days=2), recurring=False)
        floor = Floor(area=self.area, number=1, floor_type=FloorType.REGULAR, open_spaces=[self.hall])
        floor.add_schedule(schedule)
        floor.add_schedule(schedule)
        self.assertEqual(floor.schedules, [schedule])
        self.assertEqual(len(floor.schedules), 1)
