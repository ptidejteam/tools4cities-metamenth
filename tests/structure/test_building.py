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










