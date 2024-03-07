from enumerations import MeasurementUnit
from measure_instruments.meter import Meter
from structure.open_space import OpenSpace
from enumerations import OpenSpaceType
from enumerations import RoomType
from enumerations import MeterType
from transducers.sensor import Sensor
from enumerations import SensorMeasure
from enumerations import SensorMeasureType
from tests.structure.base_test import BaseTest


class TestRoom(BaseTest):

    def test_classroom_with_name_and_area(self):
        self.assertEqual(self.room.room_type, RoomType.BEDROOM)
        self.assertEqual(self.room.area.value, 45)
        self.assertEqual(self.room.area.measurement_unit, MeasurementUnit.SQUARE_METERS)
        self.assertEqual(self.room.name, "Room 145")
        self.assertEqual(self.room.location, "")
        self.assertIsNone(self.room.meter)

    def test_classroom_with_power_meter_with_different_location(self):
        try:
            power_meter = Meter("huz.cab.err", "Honeywell", 5, MeasurementUnit.KILOWATTS, MeterType.POWER)
            self.room.meter = power_meter
        except ValueError as err:
            self.assertEqual(err.__str__(), "what3words location of meter should be the same as space")

    def test_classroom_with_power_meter_and_same_location(self):
        self.room.location = "huz.cab.err"
        power_meter = Meter("huz.cab.err", "Honeywell", 5, MeasurementUnit.KILOWATTS, MeterType.POWER)
        power_meter.add_meter_measure(2)
        power_meter.add_meter_measure(5)
        self.room.meter = power_meter
        self.assertEqual(self.room.meter.meter_type, power_meter.meter_type)
        self.assertEqual(len(self.room.meter.meter_measures), 2)
        self.assertEqual(self.room.location, power_meter.meter_location)

    def test_classroom_with_adjacent_hall(self):
        hall = OpenSpace("LECTURE_HALL_2", self.area, OpenSpaceType.HALL)
        self.room.add_adjacent_space(hall)
        self.assertEqual(len(self.room.adjacent_spaces), 1)
        self.assertEqual(self.room.adjacent_spaces[0], hall)
        self.assertEqual(self.room.adjacent_spaces[0].space_type, OpenSpaceType.HALL)

    def test_classroom_as_adjacent_room_to_hall(self):
        self.hall = OpenSpace("LECTURE_HALL_3", self.area, OpenSpaceType.HALL)
        self.room.add_adjacent_space(self.hall)
        self.hall.add_adjacent_space(self.room)
        self.assertEqual(self.hall.adjacent_spaces[0], self.room)
        self.assertEqual(self.hall.adjacent_spaces[0].room_type, RoomType.BEDROOM)

    def test_remove_adjacent_space(self):
        self.hall = OpenSpace("LECTURE_HALL_4", self.area, OpenSpaceType.HALL)
        self.room.add_adjacent_space(self.hall)
        self.assertEqual(self.room.adjacent_spaces[0], self.hall)

        self.room.remove_adjacent_space(self.hall)
        self.assertEqual(self.room.adjacent_spaces, [])

    def test_add_existing_adjacent_space(self):
        self.hall = OpenSpace("LECTURE_HALL_5", self.area, OpenSpaceType.HALL)
        self.room.add_adjacent_space(self.hall)
        self.room.add_adjacent_space(self.hall)
        # should not add an adjacent space that already exists
        self.assertEqual(len(self.room.adjacent_spaces), 1)
        self.assertEqual(self.room.adjacent_spaces, [self.hall])

    def test_classroom_with_co2_and_temp_sensors(self):
        co2_sensor = Sensor("Co2_Sensor", SensorMeasure.CARBON_DIOXIDE,
                            MeasurementUnit.PARTS_PER_MILLION, SensorMeasureType.PT_100, 5)
        temp_sensor = Sensor("Temp_Sensor", SensorMeasure.TEMPERATURE,
                             MeasurementUnit.DEGREE_CELSIUS, SensorMeasureType.PT_100, 5)
        self.room.add_transducer(co2_sensor)
        self.room.add_transducer(temp_sensor)
        self.assertEqual(len(self.room.transducers), 2)
        self.assertEqual(self.room.transducers[0].measure, SensorMeasure.CARBON_DIOXIDE)
        self.assertEqual(self.room.transducers[1].measure, SensorMeasure.TEMPERATURE)
        self.assertEqual(self.room.transducers[0].data_frequency, self.room.transducers[1].data_frequency)

    def test_add_existing_sensor_with_the_same_name(self):
        co2_sensor = Sensor("Co2_Sensor", SensorMeasure.CARBON_DIOXIDE,
                            MeasurementUnit.PARTS_PER_MILLION, SensorMeasureType.PT_100, 5)
        temp_sensor = Sensor("Co2_Sensor", SensorMeasure.TEMPERATURE,
                             MeasurementUnit.DEGREE_CELSIUS, SensorMeasureType.PT_100, 8)
        self.room.add_transducer(co2_sensor)
        self.room.add_transducer(temp_sensor)

        self.assertEqual(len(self.room.transducers), 1)
        self.assertEqual(self.room.transducers[0].data_frequency, 5)

    def test_remove_transducer_from_room(self):
        co2_sensor = Sensor("Co2_Sensor", SensorMeasure.CARBON_DIOXIDE,
                            MeasurementUnit.PARTS_PER_MILLION, SensorMeasureType.PT_100, 5)
        temp_sensor = Sensor("Temp_Sensor", SensorMeasure.TEMPERATURE,
                             MeasurementUnit.DEGREE_CELSIUS, SensorMeasureType.PT_100, 5)
        self.room.add_transducer(co2_sensor)
        self.room.add_transducer(temp_sensor)
        self.assertEqual(len(self.room.transducers), 2)

        self.room.remove_transducer(co2_sensor)

        self.assertEqual(len(self.room.transducers), 1)
        self.assertEqual(self.room.transducers[0], temp_sensor)

        self.room.remove_transducer(temp_sensor)
        self.assertEqual(len(self.room.transducers), 0)

