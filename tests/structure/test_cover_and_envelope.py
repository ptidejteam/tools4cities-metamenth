from structure.layer import Layer
from structure.cover import Cover
from structure.envelope import Envelope
from enumerations import CoverType
import copy
from tests.structure.base_test import BaseTest
from enumerations import MaterialType


class TestCoverAndEnvelop(BaseTest):

    def test_floor_cover_without_layers(self):
        cover = Cover(CoverType.FLOOR)
        self.assertEqual(cover.cover_type, CoverType.FLOOR)
        self.assertIsNotNone(cover.UID)
        self.assertEqual(cover.get_layers(), [])
        self.assertEqual(len(cover.get_layers()), 0)

    def test_floor_cover_without_cover_type(self):
        try:
            cover = Cover(None)
            self.assertEqual(cover.cover_type, None)
            self.assertIsNotNone(cover.UID)
        except ValueError as err:
            self.assertEqual(err.__str__(), "cover_type must be of type CoverType")

    def test_floor_cover_with_roof_layer(self):
        try:
            cover = Cover(CoverType.FLOOR)
            cover.add_layer(self.layer)
        except ValueError as err:
            self.assertEqual(err.__str__(), "The layer you're trying to add has a different material from the cover.")

    def test_roof_cover_with_roof_layer(self):
        cover = Cover(CoverType.ROOF)
        cover.add_layer(self.layer)
        self.assertEqual(cover.get_layer_by_uid(self.layer.UID), self.layer)
        self.assertEqual(cover.get_layer_by_uid(self.layer.UID).material.heat_capacity, self.hc_measure)

    def test_roof_cover_with_two_layers(self):
        cover = Cover(CoverType.ROOF)
        cover.add_layer(self.layer)
        new_layer = copy.deepcopy(self.layer)
        new_layer.has_vapour_barrier = True
        cover.add_layer(new_layer)
        self.assertEqual(cover.get_layers()[1].has_vapour_barrier, True)
        self.assertEqual(len(cover.get_layers()), 2)

    def test_empty_envelope(self):
        envelope = Envelope()
        self.assertIsNotNone(envelope.UID)
        self.assertEqual(envelope.get_covers(), [])

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
        self.assertEqual(envelope.get_cover_by_uid(cover.UID), cover)
        self.assertIsInstance(envelope.get_cover_by_uid(cover.UID), Cover)
        self.assertIsInstance(envelope.get_cover_by_uid(cover.UID).get_layer_by_uid(self.layer.UID), Layer)
        self.assertEqual(envelope.get_cover_by_uid(cover.UID).cover_type, CoverType.ROOF)
        self.assertEqual(len(envelope.get_cover_by_uid(cover.UID).get_layers()), 2)

    def test_get_layer_by_uid(self):
        cover = Cover(CoverType.ROOF)
        cover.add_layer(self.layer)
        new_layer = Layer(self.height, self.length, self.width, self.ex_material)
        new_layer.has_vapour_barrier = True
        cover.add_layer(new_layer)
        layer = cover.get_layer_by_uid(new_layer.UID)
        self.assertEqual(layer, new_layer)

    def test_get_layer_with_wrong_uid(self):
        cover = Cover(CoverType.ROOF)
        cover.add_layer(self.layer)
        new_layer = Layer(self.height, self.length, self.width, self.ex_material)
        new_layer.has_vapour_barrier = True
        cover.add_layer(new_layer)
        layer = cover.get_layer_by_uid(cover.UID)
        self.assertEqual(layer, None)

    def test_search_layers_with_wrong_values(self):
        cover = Cover(CoverType.ROOF)
        cover.add_layer(self.layer)
        new_layer = Layer(self.height, self.length, self.width, self.ex_material)
        new_layer.has_vapour_barrier = True
        cover.add_layer(new_layer)
        layers = cover.get_layers({'height': self.width, 'thickness': self.length})
        self.assertEqual(layers, [])

    def test_search_layers_with_wrong_attributes(self):
        cover = Cover(CoverType.ROOF)
        cover.add_layer(self.layer)
        new_layer = Layer(self.height, self.length, self.width, self.ex_material)
        new_layer.has_vapour_barrier = True
        cover.add_layer(new_layer)
        layers = cover.get_layers({'width': self.width, 'area': self.length})
        self.assertEqual(layers, [])

    def test_search_layers(self):
        cover = Cover(CoverType.ROOF)
        cover.add_layer(self.layer)
        new_layer = Layer(self.height, self.length, self.width, self.ex_material)
        new_layer.has_vapour_barrier = True
        cover.add_layer(new_layer)
        layers = cover.get_layers({'height': self.height, 'thickness': self.width})
        self.assertEqual(layers, [self.layer, new_layer])

    def test_get_cover_by_uid(self):
        first_cover = Cover(CoverType.ROOF)
        first_cover.add_layer(self.layer)

        second_cover = Cover(CoverType.WINDOW)
        material = copy.deepcopy(self.ex_material)

        material.material_type = MaterialType.WIN_DOOR_WOOD
        new_layer = Layer(self.height, self.length, self.width, material)
        second_cover.add_layer(new_layer)

        envelope = Envelope()
        envelope.add_cover(first_cover)
        envelope.add_cover(second_cover)

        self.assertEqual(envelope.get_cover_by_uid(first_cover.UID), first_cover)
        self.assertEqual(envelope.get_cover_by_uid(second_cover.UID), second_cover)

    def test_get_cover_with_wrong_uid(self):
        cover = Cover(CoverType.ROOF)
        cover.add_layer(self.layer)

        envelope = Envelope()
        envelope.add_cover(cover)

        self.assertIsNone(envelope.get_cover_by_uid(self.layer.UID))
        self.assertNotEqual(envelope.get_cover_by_uid(self.layer.UID), cover)

    def test_search_covers_with_wrong_attributes(self):
        first_cover = Cover(CoverType.ROOF)
        first_cover.add_layer(self.layer)

        second_cover = Cover(CoverType.WINDOW)
        material = copy.deepcopy(self.ex_material)

        material.material_type = MaterialType.WIN_DOOR_WOOD
        new_layer = Layer(self.height, self.length, self.width, material)
        second_cover.add_layer(new_layer)

        envelope = Envelope()
        envelope.add_cover(first_cover)
        envelope.add_cover(second_cover)

        covers = envelope.get_covers({'name': 'RoofCover'})
        self.assertEqual(covers, [])

    def test_search_covers(self):
        first_cover = Cover(CoverType.ROOF)
        first_cover.add_layer(self.layer)

        second_cover = Cover(CoverType.WINDOW)
        material = copy.deepcopy(self.ex_material)

        material.material_type = MaterialType.WIN_DOOR_WOOD
        new_layer = Layer(self.height, self.length, self.width, material)
        second_cover.add_layer(new_layer)

        envelope = Envelope()
        envelope.add_cover(first_cover)
        envelope.add_cover(second_cover)

        covers = envelope.get_covers({'cover_type': CoverType.WINDOW})
        self.assertEqual(covers, [second_cover])



