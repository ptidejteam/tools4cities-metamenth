from enumerations import MeasurementUnit
from structure.open_space import OpenSpace
from enumerations import OpenSpaceType
import copy
from tests.structure.base_test import BaseTest
from transducers.sensor import Sensor
from enumerations import SensorMeasure
from enumerations import SensorMeasureType


class TestOpenSpace(BaseTest):

    def test_open_space_with_no_adjacent_spaces_and_zones(self):
        self.assertEqual(self.hall.adjacent_spaces, [])
        self.assertEqual(self.hall.zones, [])
        self.assertIsNotNone(self.hall.UID)
        self.assertEqual(self.hall.area.value, 45)
        self.assertEqual(self.hall.area.measurement_unit, MeasurementUnit.SQUARE_METERS)

    def test_open_space_with_adjacent_space(self):
        dinning_area = copy.deepcopy(self.hall)
        dinning_area.space_type = OpenSpaceType.DINNING_AREA
        self.hall.add_adjacent_space(dinning_area)
        self.assertEqual(self.hall.adjacent_spaces[0], dinning_area)
        self.assertEqual(self.hall.adjacent_spaces[0].space_type, OpenSpaceType.DINNING_AREA)
        self.assertEqual(len(self.hall.adjacent_spaces), 1)

    def test_open_space_with_no_space_type(self):
        try:
            OpenSpace("HALL_2", self.area, None)
        except ValueError as err:
            self.assertEqual(err.__str__(), "space_type must be of type OpenSpaceType")

    def test_open_space_with_none_area(self):
        try:
            self.hall.area = None
        except ValueError as err:
            self.assertEqual(err.__str__(), "area must be of type BinaryMeasure")
            self.assertEqual(self.hall.area, self.area)

    def test_open_space_with_co2_sensor(self):
        co2_sensor = Sensor("Co2_Sensor", SensorMeasure.CARBON_DIOXIDE,
                            MeasurementUnit.PARTS_PER_MILLION, SensorMeasureType.PT_100, 5)
        self.hall.add_transducer(co2_sensor)
        self.assertEqual(self.hall.transducers, [co2_sensor])
        self.assertEqual(self.hall.transducers[0].name, "Co2_Sensor")
