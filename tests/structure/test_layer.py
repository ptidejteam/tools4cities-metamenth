from unittest import TestCase
from metamenth.enumerations import MaterialType
from metamenth.structure.material import Material
from metamenth.structure.layer import Layer
from metamenth.misc import MeasureFactory
from metamenth.enumerations import RecordingType
from metamenth.datatypes.measure import Measure
from metamenth.enumerations import MeasurementUnit
from metamenth.enumerations import LayerRoughness


class TestLayer(TestCase):

    def setUp(self) -> None:
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
            material_type=MaterialType.EX_WALL_BRICK,
            density=density_measure,
            heat_capacity=self.hc_measure,
            thermal_transmittance=tt_measure,
            thermal_resistance=tr_measure,
            thermal_absorptance=0.8,
            solar_absorptance=0.6
        )

        height = MeasureFactory.create_measure(RecordingType.BINARY.value, Measure(MeasurementUnit.METERS, 20))
        length = MeasureFactory.create_measure(RecordingType.BINARY.value, Measure(MeasurementUnit.METERS, 15))
        width = MeasureFactory.create_measure(RecordingType.BINARY.value, Measure(MeasurementUnit.METERS, 3))
        self.layer = Layer(height, length, width, self.ex_material, LayerRoughness.ROUGH)

    def test_layer_with_external_material(self):
        self.assertEqual(self.layer.has_air_barrier, False)
        self.assertEqual(self.layer.has_vapour_barrier, False)
        self.assertEqual(self.layer.height.measurement_unit.value, MeasurementUnit.METERS.value)
        self.assertEqual(self.layer.material.heat_capacity.measurement_unit.value,
                         self.hc_measure.measurement_unit.value)
        self.assertEqual(self.layer.material, self.ex_material)
        self.assertIsNotNone(self.layer.UID)

    def test_layer_with_no_material(self):
        try:
            self.layer.material = None
            self.assertIsNone(self.layer.material)
        except ValueError as err:
            self.assertEqual(err.__str__(), "material cannot be None")

    def test_layer_with_internal_material(self):
        self.ex_material.material_type = MaterialType.IN_WALL_CELLULOSE
        self.layer.material = self.ex_material
        self.assertEqual(self.layer.material.material_type, MaterialType.IN_WALL_CELLULOSE)
        self.assertEqual(self.layer.material, self.ex_material)
