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
from metamenth.structure.layer import Layer
from metamenth.structure.material import Material
from metamenth.enumerations import MaterialType
from metamenth.enumerations import ApplianceType
from metamenth.enumerations import ApplianceCategory
from metamenth.subsystem.appliance import Appliance
from metamenth.enumerations import SensorLogType
from metamenth.transducers.sensor import Sensor
from metamenth.enumerations import SensorMeasure
from metamenth.enumerations import SensorMeasureType
from metamenth.enumerations import LayerRoughness


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

        density_measure = MeasureFactory.create_measure(RecordingType.BINARY.value,
                                                        Measure(MeasurementUnit.KILOGRAM_PER_CUBIC_METER, 0.5))
        self.hc_measure = MeasureFactory.create_measure(RecordingType.BINARY.value,
                                                        Measure(MeasurementUnit.JOULES_PER_KELVIN, 4.5))
        tt_measure = MeasureFactory.create_measure(RecordingType.BINARY.value,
                                                   Measure(MeasurementUnit.WATTS_PER_SQUARE_METER_KELVIN, 2.5))
        tr_measure = MeasureFactory.create_measure(RecordingType.BINARY.value,
                                                   Measure(MeasurementUnit.SQUARE_METERS_KELVIN_PER_WATTS,
                                                           2.3))
        self.ex_material = Material(
            description="Material for the external wall of a building",
            material_type=MaterialType.ROOF_STEEL,
            density=density_measure,
            heat_capacity=self.hc_measure,
            thermal_transmittance=tt_measure,
            thermal_resistance=tr_measure
        )

        self.height = MeasureFactory.create_measure(RecordingType.BINARY.value, Measure(MeasurementUnit.METERS, 20))
        self.length = MeasureFactory.create_measure(RecordingType.BINARY.value, Measure(MeasurementUnit.METERS, 15))
        self.width = MeasureFactory.create_measure(RecordingType.BINARY.value, Measure(MeasurementUnit.METERS, 3))
        self.layer = Layer(self.height, self.length, self.width, self.ex_material, LayerRoughness.MEDIUM_ROUGH)

        # Thermostat
        self.thermostat = Appliance("Thermostat", [ApplianceCategory.OFFICE, ApplianceCategory.SMART],
                                    ApplianceType.THERMOSTAT)
        self.temp_sensor = Sensor("TEMPERATURE.SENSOR", SensorMeasure.TEMPERATURE, MeasurementUnit.DEGREE_CELSIUS,
                                  SensorMeasureType.THERMO_COUPLE_TYPE_A, 900, sensor_log_type=SensorLogType.POLLING)
        self.presence_sensor = Sensor("PRESENCE.SENSOR", SensorMeasure.OCCUPANCY, MeasurementUnit.PRESENCE,
                                      SensorMeasureType.THERMO_COUPLE_TYPE_A, 0, sensor_log_type=SensorLogType.POLLING)
        self.thermostat.add_transducer(self.presence_sensor)
        self.thermostat.add_transducer(self.temp_sensor)

        # Smart Camera
        self.smart_camera = Appliance("Smart Camera", [ApplianceCategory.OFFICE, ApplianceCategory.SMART],
                                      ApplianceType.CAMERA)

        self.smart_camera.add_transducer(self.presence_sensor)
