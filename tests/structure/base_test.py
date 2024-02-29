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
from structure.layer import Layer
from structure.material import Material
from enumerations import MaterialType


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
        self.layer = Layer(self.height, self.length, self.width, self.ex_material)
