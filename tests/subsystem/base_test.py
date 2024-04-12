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
from structure.building import Building
from enumerations import BuildingType
from datatypes.address import Address
from enumerations import SensorLogType
from transducers.sensor import Sensor
from enumerations import SensorMeasure
from enumerations import SensorMeasureType


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



