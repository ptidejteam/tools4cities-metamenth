from unittest import TestCase
from misc import MeasureFactory
from enumerations import RecordingType
from datatypes.measure import Measure
from enumerations import MeasurementUnit
from structure.open_space import OpenSpace
from enumerations import OpenSpaceType
import copy
from datatypes.zone import Zone
from enumerations import ZoneType
from enumerations import HVACType


class TestOpenSpace(TestCase):

    def setUp(self) -> None:
        self.area = MeasureFactory.create_measure(RecordingType.BINARY.value,
                                                  Measure(MeasurementUnit.SQUARE_METER, 30))
        self.hall = OpenSpace(self.area, OpenSpaceType.HALL)

    def test_open_space_with_no_adjacent_spaces_and_zones(self):
        self.assertEqual(self.hall.adjacent_spaces, [])
        self.assertEqual(self.hall.zones, [])
        self.assertIsNotNone(self.hall.UID)
        self.assertEqual(self.hall.area.value, 30)
        self.assertEqual(self.hall.area.measurement_unit, MeasurementUnit.SQUARE_METER)

    def test_open_space_with_adjacent_space(self):
        dinning_area = copy.deepcopy(self.hall)
        dinning_area.space_type = OpenSpaceType.DINNING_AREA
        self.hall.add_adjacent_space(dinning_area)
        self.assertEqual(self.hall.adjacent_spaces[0], dinning_area)
        self.assertEqual(self.hall.adjacent_spaces[0].space_type, OpenSpaceType.DINNING_AREA)
        self.assertEqual(len(self.hall.adjacent_spaces), 1)

    def test_open_space_with_adjacent_space_and_zone(self):
        zone = Zone('HVAC ZONE', ZoneType.HVAC)
        zone.hvac_type = HVACType.INTERIOR
        dinning_area = copy.deepcopy(self.hall)
        dinning_area.space_type = OpenSpaceType.DINNING_AREA
        self.hall.add_adjacent_space(dinning_area)
        self.hall.add_zone(zone)
        self.assertEqual(self.hall.zones[0], zone)
        self.assertEqual(self.hall.adjacent_spaces[0], dinning_area)
        self.assertEqual(self.hall.zones[0].zone_type, ZoneType.HVAC)
        self.assertEqual(self.hall.zones[0].hvac_type, HVACType.INTERIOR)

    def test_open_space_with_no_space_type(self):
        try:
            space = OpenSpace(self.area, None)
        except ValueError as err:
            self.assertEqual(err.__str__(), "space_type must be of type OpenSpaceType")

    def test_open_space_with_none_area(self):
        try:
            self.hall.area = None
        except ValueError as err:
            self.assertEqual(err.__str__(), "area must be of type BinaryMeasure")
            self.assertEqual(self.hall.area, self.area)
