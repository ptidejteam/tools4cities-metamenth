import uuid
from enumerations import CoverType
from structure import Layer
from typing import List


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
        self.UID = str(uuid.uuid4())
        self.cover_type = cover_type
        self.layers: List['Layer'] = [] # the various layers in this building cover

    def add_layer(self, layer: Layer):
        """
        Add a layer (e.g., external wall) to the building cover e.g., wall
        :param layer: the layer to be added
        :return:
        """
        if layer.material.material_type.value.split(":")[0].find(self.cover_type.value) != -1:
            self.layers.append(layer)
        else:
            raise ValueError("The layer you're trying to add has a different material from the cover.")

    def __str__(self):
        layer_str = "\n".join(str(layer) for layer in self.layers)
        return (
            f"Cover("
            f"UID: {self.UID}, "
            f"Cover Type: {self.cover_type}, "
            f"Layers:\n{layer_str})"
        )
