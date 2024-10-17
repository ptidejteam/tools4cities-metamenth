from unittest import TestCase
from enumerations import MaterialType
from structure.material import Material
from misc import MeasureFactory
from enumerations import RecordingType
from datatypes.measure import Measure
from enumerations import MeasurementUnit


class TestMaterial(TestCase):

    def setUp(self) -> None:
        self.density_measure = MeasureFactory.create_measure(RecordingType.BINARY.value,
                                                             Measure(MeasurementUnit.KILOGRAM_PER_CUBIC_METER, 0.5))
        self.hc_measure = MeasureFactory.create_measure(RecordingType.BINARY.value,
                                                        Measure(MeasurementUnit.JOULES_PER_KELVIN, 4.5))
        self.tt_measure = MeasureFactory.create_measure(RecordingType.BINARY.value,
                                                        Measure(MeasurementUnit.WATTS_PER_SQUARE_METER_KELVIN, 2.5))
        self.material = None

    def test_material_without_thermal_resistance(self):

        with self.assertRaises(TypeError) as context:
            self.material = Material(
                description="Material for the external wall of a building",
                material_type=MaterialType.EX_WALL_BRICK,
                density=self.density_measure,
                heat_capacity=self.hc_measure,
                thermal_transmittance=self.tt_measure
            )
            self.assertEqual(str(context.exception),
                             "__init__() missing 1 required positional argument: 'thermal_resistance'")

    def test_valid_material(self):

        tr_measure = MeasureFactory.create_measure(RecordingType.BINARY.value,
                                                   Measure(MeasurementUnit.SQUARE_METERS_KELVIN_PER_WATTS,
                                                           2.3))
        self.material = Material(
            description="Material for the external wall of a building",
            material_type=MaterialType.EX_WALL_BRICK,
            density=self.density_measure,
            heat_capacity=self.hc_measure,
            thermal_transmittance=self.tt_measure,
            thermal_resistance=tr_measure
        )
        # Test UID is not empty and that it's generated automatically
        self.assertTrue(self.material.UID)

        # Test other attributes
        self.assertEqual(self.material.thermal_transmittance, self.tt_measure)
        self.assertEqual(self.material.material_type, MaterialType.EX_WALL_BRICK)
        self.assertEqual(self.material.thermal_resistance, tr_measure)
        self.assertEqual(self.material.visible_absorptance, None)

    def test_material_with_invalid_absorptance(self):

        tr_measure = MeasureFactory.create_measure(RecordingType.BINARY.value,
                                                   Measure(MeasurementUnit.SQUARE_METERS_KELVIN_PER_WATTS, 2.3))
        try:
            self.material = Material(
                description="Material for the external wall of a building",
                material_type=MaterialType.EX_WALL_BRICK,
                density=self.density_measure,
                heat_capacity=self.hc_measure,
                thermal_transmittance=self.tt_measure,
                thermal_resistance=tr_measure,
                thermal_absorptance=2.5
            )
        except ValueError as err:
            self.assertEqual(err.__str__(), "2.5 must be a number between 0 and 1.")

    def test_material_with_none_thermal_resistance(self):
        try:
            self.material = Material(
                description="Material for the external wall of a building",
                material_type=MaterialType.EX_WALL_BRICK,
                density=self.density_measure,
                heat_capacity=self.hc_measure,
                thermal_transmittance=self.tt_measure,
                thermal_resistance=None
            )

        except ValueError as err:
            self.assertEqual(err.__str__(), "thermal_resistance must be of type BinaryMeasure")
