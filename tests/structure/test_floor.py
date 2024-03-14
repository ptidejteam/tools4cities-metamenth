from enumerations import OpenSpaceType
from structure.floor import Floor
from enumerations import FloorType
from datatypes.operational_schedule import OperationalSchedule
from datetime import datetime
from datetime import timedelta
from tests.structure.base_test import BaseTest
from structure.open_space import OpenSpace
from structure.room import Room
from enumerations import RoomType


class TestFloor(BaseTest):

    def test_floor_with_no_room_and_open_space(self):
        try:
            Floor(self.area, 1, FloorType.REGULAR)
        except ValueError as err:
            self.assertEqual(err.__str__(), "A floor must have at least one room or one open space.")

    def test_floor_with_one_room_and_no_open_space(self):
        self.assertEqual(self.floor.get_room_by_name(self.room.name), self.room)
        self.assertEqual(len(self.floor.get_rooms()), 1)
        self.assertEqual(len(self.floor.get_open_spaces()), 0)

    def test_floor_with_one_room_and_one_open_space(self):
        floor = Floor(area=self.area, number=1, floor_type=FloorType.REGULAR,
                      rooms=[self.room], open_spaces=[self.hall])
        self.assertEqual(floor.get_rooms(), [self.room])
        self.assertEqual(floor.get_open_spaces(), [self.hall])
        self.assertEqual(floor.get_open_space_by_name(self.hall.name).space_type, OpenSpaceType.HALL)

    def test_remove_room_from_floor(self):
        floor = Floor(area=self.area, number=1, floor_type=FloorType.REGULAR,
                      rooms=[self.room], open_spaces=[self.hall])
        self.assertEqual(floor.get_room_by_name(self.room.name), self.room)
        self.assertEqual(len(floor.get_rooms()), 1)
        # Remove rooms
        floor.remove_room(self.room)
        # Assert no rooms
        self.assertEqual(floor.get_rooms(), [])

    def test_remove_open_space_from_floor(self):
        floor = Floor(area=self.area, number=1, floor_type=FloorType.REGULAR, open_spaces=[self.hall])
        self.assertEqual(floor.get_open_space_by_name(self.hall.name), self.hall)
        # Remove open space
        floor.remove_open_space(self.hall)
        # Assert no open space
        self.assertEqual(floor.get_open_spaces(), [])

    def test_add_floor_recurring_operational_schedule(self):
        schedule = OperationalSchedule("WEEKDAYS", datetime.now(), datetime.now() + timedelta(days=5))
        floor = Floor(area=self.area, number=1, floor_type=FloorType.REGULAR, open_spaces=[self.hall])
        floor.add_schedule(schedule)
        self.assertEqual(floor.get_schedules(), [schedule])
        self.assertEqual(floor.get_schedule_by_name(schedule.name).recurring, True)

    def test_add_floor_non_recurring_operational_schedule(self):
        schedule = OperationalSchedule("WEEKENDS", datetime.now(), datetime.now() + timedelta(days=2), recurring=False)
        floor = Floor(area=self.area, number=1, floor_type=FloorType.REGULAR, open_spaces=[self.hall])
        floor.add_schedule(schedule)
        self.assertEqual(floor.get_schedules(), [schedule])
        self.assertEqual(floor.get_schedule_by_name(schedule.name).recurring, False)

    def test_add_existing_schedule_to_floor(self):
        schedule = OperationalSchedule("WEEKENDS", datetime.now(), datetime.now() + timedelta(days=2), recurring=False)
        floor = Floor(area=self.area, number=1, floor_type=FloorType.REGULAR, open_spaces=[self.hall])
        floor.add_schedule(schedule)
        floor.add_schedule(schedule)
        self.assertEqual(floor.get_schedules(), [schedule])
        self.assertEqual(len(floor.get_schedules()), 1)

    def test_get_room_by_uid(self):
        floor = Floor(area=self.area, number=1, floor_type=FloorType.REGULAR, rooms=[self.room])
        room = floor.get_room_by_uid(self.room.UID)
        self.assertEqual(room, self.room)

    def test_get_room_with_wrong_uid(self):
        floor = Floor(area=self.area, number=1, floor_type=FloorType.REGULAR, rooms=[self.room])
        room = floor.get_room_by_uid(self.hall.UID)
        self.assertEqual(room, None)

    def test_get_room_by_name(self):
        floor = Floor(area=self.area, number=1, floor_type=FloorType.REGULAR, rooms=[self.room])
        room = floor.get_room_by_name(self.room.name)
        self.assertEqual(room, self.room)

    def test_get_room_with_wrong_name(self):
        floor = Floor(area=self.area, number=1, floor_type=FloorType.REGULAR, rooms=[self.room])
        room = floor.get_room_by_name(self.hall.name)
        self.assertEqual(room, None)

    def test_get_open_space_by_uid(self):
        corridor = OpenSpace("CORRIDOR", self.area, OpenSpaceType.CORRIDOR)
        floor = Floor(area=self.area, number=1, floor_type=FloorType.REGULAR, open_spaces=[self.hall, corridor])
        open_space = floor.get_open_space_by_uid(corridor.UID)
        self.assertEqual(open_space, corridor)

    def test_get_open_space_with_wrong_uid(self):
        corridor = OpenSpace("CORRIDOR", self.area, OpenSpaceType.CORRIDOR)
        floor = Floor(area=self.area, number=1, floor_type=FloorType.REGULAR, rooms=[self.hall, corridor])
        room = floor.get_open_space_by_uid(self.room.UID)
        self.assertEqual(room, None)

    def test_get_open_space_by_name(self):
        corridor = OpenSpace("CORRIDOR", self.area, OpenSpaceType.CORRIDOR)
        floor = Floor(area=self.area, number=1, floor_type=FloorType.REGULAR, open_spaces=[self.hall, corridor])
        open_space = floor.get_open_space_by_name(corridor.name)
        self.assertEqual(open_space, corridor)

    def test_get_open_space_with_wrong_name(self):
        corridor = OpenSpace("CORRIDOR", self.area, OpenSpaceType.CORRIDOR)
        floor = Floor(area=self.area, number=1, floor_type=FloorType.REGULAR, open_spaces=[self.hall, corridor])
        open_space = floor.get_open_space_by_uid(self.room.name)
        self.assertEqual(open_space, None)

    def test_search_rooms_with_wrong_search_terms(self):
        lavatory = Room(self.area, "Lav 002", RoomType.LAVATORY)
        floor = Floor(area=self.area, number=1, floor_type=FloorType.REGULAR, rooms=[lavatory, self.room])
        try:
            floor.get_rooms({'name': 'Lav 002', 'space_type': 'large'})
        except AttributeError as err:
            self.assertEqual(err.__str__(), "'Room' object has no attribute 'space_type'")

    def test_search_rooms(self):
        room = Room(self.area, "Room 444", RoomType.BEDROOM)
        floor = Floor(area=self.area, number=1, floor_type=FloorType.REGULAR, rooms=[room, self.room])
        rooms = floor.get_rooms({'room_type': RoomType.BEDROOM})
        self.assertEqual(rooms, [room, self.room])

    def test_search_open_spaces_with_wrong_search_terms(self):
        corridor = OpenSpace("CORRIDOR", self.area, OpenSpaceType.CORRIDOR)
        floor = Floor(area=self.area, number=1, floor_type=FloorType.REGULAR, open_spaces=[corridor, self.hall])
        try:
            floor.get_open_spaces({'name': 'CORRIDOR', 'size': 'large'})
        except AttributeError as err:
            self.assertEqual(err.__str__(), "'OpenSpace' object has no attribute 'size'")

    def test_search_open_spaces(self):
        hall = OpenSpace("HALL_ONE", self.area, OpenSpaceType.HALL)
        floor = Floor(area=self.area, number=1, floor_type=FloorType.REGULAR, open_spaces=[hall, self.hall])
        open_spaces = floor.get_open_spaces({'space_type': OpenSpaceType.HALL})
        self.assertEqual(open_spaces, [hall, self.hall])


