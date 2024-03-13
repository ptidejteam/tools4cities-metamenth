from typing import List
from .abstract_space import AbstractSpace
from datatypes.interfaces.abstract_measure import AbstractMeasure
from utils import EntityRemover
from utils import EntityInsert
from measure_instruments.meter import Meter
from utils import StructureEntitySearch
from typing import Dict
from datatypes.interfaces.dynamic_entity import DynamicEntity


class AbstractFloorSpace(AbstractSpace, DynamicEntity):
    """
    An abstract class for spaces on a floor

    Author: Peter Yefi
    Email: peteryefi@gmail.com
    """

    def __init__(self, area: AbstractMeasure, name: str, location: str = None, meter: Meter = None):
        """
        Models spaces on a building's floor
        :param area: the area of the space
        :param name: the name of the space
        :param location: the what3word location of the space
        """
        AbstractSpace.__init__(self, area, location)
        DynamicEntity.__init__(self)

        self._name = None
        self._adjacent_spaces: List[AbstractFloorSpace] = []
        self._meter = meter
        # apply validation through setters
        self.name = name

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        if value is not None:
            self._name = value
        else:
            raise ValueError("name must be a string")

    @property
    def meter(self) -> Meter:
        return self._meter

    @meter.setter
    def meter(self, value: Meter):
        if value:
            if value.meter_location != self.location:
                raise ValueError("what3words location of meter should be the same as space")
        self._meter = value

    def add_adjacent_space(self, space: 'AbstractFloorSpace'):
        """
        specifies (adds) which spaces (room and open spaces) are adjacent to other spaces
        :param space:
        :return:
        """
        EntityInsert.insert_building_entity(self._adjacent_spaces, space)

    def remove_adjacent_space(self, adjacent_space: 'AbstractFloorSpace'):
        """
        Removes adjacent space from a space (room and open space)
        :param adjacent_space: the adjacent space to remove
        :return:
        """
        EntityRemover.remove_building_entity(self._adjacent_spaces, adjacent_space)

    def get_adjacent_space_by_name(self, name) -> 'AbstractFloorSpace':
        """
        Search adjacent spaces by name
        :param name:  the name of the zone
        :return:
        """
        return StructureEntitySearch.search_by_name(self._adjacent_spaces, name)

    def get_adjacent_space_by_uid(self, uid) -> 'AbstractFloorSpace':
        """
        Search adjacent spaces by uid
        :param uid: the unique identifier of the adjacent spaces
        :return:
        """
        return StructureEntitySearch.search_by_id(self._adjacent_spaces, uid)

    def get_adjacent_spaces(self, search_terms: Dict) -> ['AbstractFloorSpace']:
        """
        Search adjacent spaces by attributes values
        :param search_terms: a dictionary of attributes and their values
        :return:
        """
        return StructureEntitySearch.search(self._adjacent_spaces, search_terms)

    def __eq__(self, other):
        # spaces on a floor are equal if they share the same name
        if isinstance(other, AbstractFloorSpace):
            # Check for equality based on the 'name' attribute
            return self.name == other.name
        return False

    def __str__(self) -> str:
        return (
            f"{super().__str__()}"
            f"Name: {self.name}, "
            f"Meter: {self.meter}, "
            f"Adjacent Spaces: {self._adjacent_spaces}, "
            f"Transducers: {self._transducers}, "
        )
