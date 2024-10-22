from unittest import TestCase
from metamenth.misc import MeasureFactory
from metamenth.enumerations import RecordingType
from metamenth.datatypes.measure import Measure
from metamenth.enumerations import MeasurementUnit
from metamenth.structure.open_space import OpenSpace
from metamenth.enumerations import OpenSpaceType
from metamenth.enumerations import RoomType
from metamenth.structure.room import Room
from metamenth.structure.floor import Floor
from metamenth.enumerations import FloorType
from metamenth.structure.building import Building
from metamenth.enumerations import BuildingType
from metamenth.datatypes.address import Address
from metamenth.enumerations import SensorLogType
from metamenth.transducers.sensor import Sensor
from metamenth.enumerations import SensorMeasure
from metamenth.enumerations import SensorMeasureType


class BaseTest(TestCase):
    def setUp(self) -> None:
        self.area = MeasureFactory.create_measure(RecordingType.BINARY.value,
                                                  Measure(MeasurementUnit.SQUARE_METERS, 45))
        self.room = Room(self.area, "Room 145", RoomType.BEDROOM)
        self.hall = OpenSpace("LECTURE_HALL_1", self.area, OpenSpaceType.HALL)
        self.address = Address("Montreal", "6399 Rue Sherbrooke", "QC", "H1N 2Z3", "Canada")
        self.floor_area = MeasureFactory.create_measure(RecordingType.BINARY.value,
                                                        Measure(MeasurementUnit.SQUARE_METERS, 5))
        self.height = MeasureFactory.create_measure(RecordingType.BINARY.value,
                                                    Measure(MeasurementUnit.METERS, 30))
        self.internal_mass = MeasureFactory.create_measure(RecordingType.BINARY.value,
                                                           Measure(MeasurementUnit.KILOGRAMS, 2000))
        self.floor = Floor(area=self.area, number=1, floor_type=FloorType.REGULAR, rooms=[self.room])
        self.building = Building(2009, self.height, self.floor_area, self.internal_mass, self.address,
                                 BuildingType.COMMERCIAL, [self.floor])

        self.presence_sensor = Sensor("PRESENCE.SENSOR", SensorMeasure.OCCUPANCY, MeasurementUnit.PRESENCE,
                                 SensorMeasureType.THERMO_COUPLE_TYPE_A, 0, sensor_log_type=SensorLogType.POLLING)
        self.temp_sensor = Sensor("TEMP.SENSOR", SensorMeasure.TEMPERATURE, MeasurementUnit.DEGREE_CELSIUS,
                             SensorMeasureType.THERMO_COUPLE_TYPE_A, 900, sensor_log_type=SensorLogType.POLLING)
        self.pressure_sensor = Sensor("PRESENCE.SENSOR", SensorMeasure.PRESSURE, MeasurementUnit.PASCAL,
                                      SensorMeasureType.THERMO_COUPLE_TYPE_A, 10, sensor_log_type=SensorLogType.POLLING)



