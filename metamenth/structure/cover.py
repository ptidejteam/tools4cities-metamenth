import uuid
from metamenth.enumerations import CoverType
from metamenth.enumerations import BuildingOrientation
from metamenth.structure.layer import Layer
from typing import List, Union
from metamenth.utils import StructureSearch
from typing import Dict


class Cover:
    """
       A building cover that forms the envelope of a building

       Author: Peter Yefi
       Email: peteryefi@gmail.com
       """

    def __init__(self, cover_type: CoverType, building_orientation: BuildingOrientation, floor_number: int):
        """
        :param cover_type: the type of building cover
        :param building_orientation: the side of the building the cover faces, e.g., south
        :param floor_number: the floor where the cover is located
        """
        self._UID = str(uuid.uuid4())
        self._cover_type = None
        self._building_orientation = None
        self._floor_number = None
        self._layers: List['Layer'] = []  # the various layers in this building cover
        self._neighbours = {'left': None, 'right': None, 'top': None, 'bottom': None}

        # validate cover type and orientation
        self.cover_type = cover_type
        self.building_orientation = building_orientation
        self.floor_number = floor_number

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
    def building_orientation(self) -> BuildingOrientation:
        return self._building_orientation

    @building_orientation.setter
    def building_orientation(self, value: BuildingOrientation):
        if value is None:
            raise ValueError("building_orientation must be of type CoverType")
        self._building_orientation = value

    @property
    def floor_number(self) -> int:
        return self._floor_number

    @floor_number.setter
    def floor_number(self, value: int):
        if value is None:
            raise ValueError("floor_number must be of type int")
        self._floor_number = value

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
        return StructureSearch.search_by_id(self._layers, uid)

    def get_layers(self, search_term: Dict = None) -> List[Layer]:
        """
        Retrieves layers given the attributes and their values
        :param search_term: the uid of the floor
        :return:
        """
        return StructureSearch.search(self._layers, search_term)

    def add_neighbour(self, cover: 'Cover', neighbour_type: str):
        """
        Adds the neighbours of a cover
        :param cover: the neighbour cover to add
        :param neighbour_type: indicates the type of neighbour, e.g., left, right, top and bottom
        """
        try:
            if self.floor_number == cover.floor_number and self.building_orientation == cover.building_orientation:
                self._neighbours[neighbour_type] = cover.UID
            else:
                raise ValueError('Neighbour covers must be on the same floor and side of building')
        except KeyError:
            print(f'Acceptable neighbour types include, left, right, top, and bottom')

    def get_neighbour(self, neighbour_type: str) -> Union[str, None]:
        """
        Gets the neighbour of a cover
        :param neighbour_type: the type of neighbour, e.g, left, right
        """
        return self._neighbours.get(neighbour_type, None)

    def __str__(self):
        layer_str = "\n".join(str(layer) for layer in self._layers)
        return (
            f"Cover("
            f"UID: {self.UID}, "
            f"Cover Type: {self.cover_type}, "
            f"Building Orientation: {self.building_orientation.value}, "
            f"Floor Number: {self.floor_number}, "
            f"Layers:\n{layer_str})"
        )
