from unittest import TestCase
from enumerations import MaterialType
from structure.material import Material
from structure.layer import Layer
from structure.cover import Cover
from structure.envelope import Envelope
from enumerations import CoverType
from misc import MeasureFactory
from enumerations import RecordingType
from datatypes.measure import Measure
from enumerations import MeasurementUnit
import copy


class TestLayerAndEnvelop(TestCase):

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
            material_type=MaterialType.ROOF_STEEL,
            density=density_measure,
            heat_capacity=self.hc_measure,
            thermal_transmittance=tt_measure,
            thermal_resistance=tr_measure
        )

        height = MeasureFactory.create_measure(RecordingType.BINARY.value, Measure(MeasurementUnit.METERS, 20))
        length = MeasureFactory.create_measure(RecordingType.BINARY.value, Measure(MeasurementUnit.METERS, 15))
        width = MeasureFactory.create_measure(RecordingType.BINARY.value, Measure(MeasurementUnit.METERS, 3))
        self.layer = Layer(height, length, width, self.ex_material)

    def test_floor_cover_without_layers(self):
        cover = Cover(CoverType.FLOOR)
        self.assertEqual(cover.cover_type, CoverType.FLOOR)
        self.assertIsNotNone(cover.UID)
        self.assertEqual(cover.layers, [])
        self.assertEqual(len(cover.layers), 0)

    def test_floor_cover_without_cover_type(self):
        try:
            cover = Cover(None)
            self.assertEqual(cover.cover_type, None)
            self.assertIsNotNone(cover.UID)
        except ValueError as err:
            self.assertEqual(err.__str__(), "cover_type is/are mandatory")

    def test_floor_cover_with_roof_layer(self):
        try:
            cover = Cover(CoverType.FLOOR)
            cover.add_layer(self.layer)
        except ValueError as err:
            self.assertEqual(err.__str__(), "The layer you're trying to add has a different material from the cover.")

    def test_roof_cover_with_roof_layer(self):
        cover = Cover(CoverType.ROOF)
        cover.add_layer(self.layer)
        self.assertEqual(cover.layers[0], self.layer)
        self.assertEqual(cover.layers[0].material.heat_capacity, self.hc_measure)

    def test_roof_cover_with_two_layers(self):
        cover = Cover(CoverType.ROOF)
        cover.add_layer(self.layer)
        new_layer = copy.deepcopy(self.layer)
        new_layer.has_vapour_barrier = True
        cover.add_layer(new_layer)
        self.assertEqual(cover.layers[1].has_vapour_barrier, True)
        self.assertEqual(len(cover.layers), 2)

    def test_empty_envelope(self):
        envelope = Envelope()
        self.assertIsNotNone(envelope.UID)
        self.assertEqual(envelope.covers, [])

    def test_envelope_with_none_cover(self):
        try:
            envelope = Envelope()
            envelope.add_cover(None)
        except ValueError as err:
            self.assertEqual(err.__str__(), "cover must be of type Cover")

    def test_envelope_with_roofing_cover_of_two_layers(self):
        cover = Cover(CoverType.ROOF)
        cover.add_layer(self.layer)
        new_layer = copy.deepcopy(self.layer)
        new_layer.has_vapour_barrier = True
        cover.add_layer(new_layer)
        envelope = Envelope()
        envelope.add_cover(cover)
        self.assertEqual(envelope.covers[0], cover)
        self.assertIsInstance(envelope.covers[0], Cover)
        self.assertIsInstance(envelope.covers[0].layers[0], Layer)
        self.assertEqual(envelope.covers[0].cover_type, CoverType.ROOF)
        self.assertEqual(len(envelope.covers[0].layers), 2)




