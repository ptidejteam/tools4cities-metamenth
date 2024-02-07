import uuid
from enumerations import CoverType
from structure.layer import Layer
from typing import List
from misc import Validate
from visitors import StructureSearch
from typing import Dict


class Cover:
    """
       A building cover that forms the envelope of a building

       Author: Peter Yefi
       Email: peteryefi@gmail.com
       """
    def __init__(self, cover_type: CoverType):
        """
        :param cover_type: the type of building cover
        """
        Validate.validate_none({"cover_type": cover_type})
        self._UID = str(uuid.uuid4())
        self._cover_type = cover_type
        self._layers: List['Layer'] = [] # the various layers in this building cover

    @property
    def UID(self) -> str:
        return self._UID

    @property
    def cover_type(self) -> CoverType:
        return self._cover_type

    @cover_type.setter
    def cover_type(self, value: CoverType):
        if value is None:
            raise ValueError("cover_type must be of type CoverType")
        self._cover_type = value

    @property
    def layers(self) -> List['Layer']:
        return self._layers

    def add_layer(self, layer: Layer):
        """
        Add a layer (e.g., external wall) to the building cover e.g., wall
        :param layer: the layer to be added
        :return:
        """
        if layer.material.material_type.value.split(":")[0].find(self.cover_type.value) != -1:
            self._layers.append(layer)
        else:
            raise ValueError("The layer you're trying to add has a different material from the cover.")

    def get_layer_by_uid(self, uid: str) -> Layer:
        """
        Retrieves a layer given the uid
        :param uid: the uid of the layer
        :return:
        """
        return StructureSearch.search_by_id(self.layers, uid)

    def get_layers(self, search_term: Dict) -> List[Layer]:
        """
        Retrieves layers given the attributes and their values
        :param search_term: the uid of the floor
        :return:
        """
        return StructureSearch.search(self.layers, search_term)

    def __str__(self):
        layer_str = "\n".join(str(layer) for layer in self.layers)
        return (
            f"Cover("
            f"UID: {self.UID}, "
            f"Cover Type: {self.cover_type}, "
            f"Layers:\n{layer_str})"
        )
