from uuid import uuid4
from metamenth.enumerations import DuctType
from metamenth.enumerations import DuctSubType
from metamenth.datatypes.interfaces.abstract_dynamic_entity import AbstractDynamicEntity
from metamenth.virtual.interfaces.abstract_zonal_entity import AbstractZonalEntity
from metamenth.subsystem.hvac_components.damper import Damper
from metamenth.subsystem.hvac_components.fan import Fan
from metamenth.subsystem.hvac_components.heat_exchanger import HeatExchanger
from typing import List
from metamenth.subsystem.hvac_components.duct_connection import DuctConnection
from metamenth.utils import EntityInsert
from metamenth.utils import EntityRemover
from metamenth.enumerations import BuildingEntity
from typing import Dict
from metamenth.utils import StructureEntitySearch
from metamenth.subsystem.hvac_components.air_volume_box import AirVolumeBox
from metamenth.subsystem.hvac_components.filter import Filter
from metamenth.subsystem.hvac_components.anemometer import Anemometer
from metamenth.datatypes.binary_measure import BinaryMeasure
from metamenth.enumerations import DuctShape
from metamenth.misc import Validate


class Duct(AbstractDynamicEntity, AbstractZonalEntity):

    def __init__(self, name: str, duct_type: DuctType):
        AbstractDynamicEntity.__init__(self)
        AbstractZonalEntity.__init__(self)
        self._UID = str(uuid4())
        self._name = None
        self._duct_type = None
        self._duct_sub_type = None
        self._connections = None
        self._length = None
        self._height = None
        self._width = None
        self._diameter = None
        self._shape = None
        self._heat_exchangers: List[HeatExchanger] = []
        self._fans: List[Fan] = []
        self._dampers: List[Damper] = []
        self._connected_air_volume_box: [AirVolumeBox] = []
        self._filters: [Filter] = []
        self._anemometers: [Anemometer] = []
        self._is_insulated = False
        self.name = name
        self.duct_type = duct_type

    @property
    def UID(self) -> str:
        return self._UID

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        if value is not None:
            self._name = value
        else:
            raise ValueError("name should be of type string")

    @property
    def is_insulated(self) -> bool:
        return self._is_insulated

    @is_insulated.setter
    def is_insulated(self, value: bool):
        self._is_insulated = value

    @property
    def length(self) -> BinaryMeasure:
        return self._length

    @length.setter
    def length(self, value: BinaryMeasure):
        self._length = value

    @property
    def width(self) -> BinaryMeasure:
        return self._width

    @width.setter
    def width(self, value: BinaryMeasure):
        self._width = value

    @property
    def height(self) -> BinaryMeasure:
        return self._height

    @height.setter
    def height(self, value: BinaryMeasure):
        self._height = value

    @property
    def shape(self) -> DuctShape:
        return self._shape

    @shape.setter
    def shape(self, value: DuctShape):
        self._shape = value

    @property
    def diameter(self) -> BinaryMeasure:
        return self._diameter

    @diameter.setter
    def diameter(self, value: BinaryMeasure):
        self._diameter = value

    @property
    def duct_type(self) -> DuctType:
        return self._duct_type

    @duct_type.setter
    def duct_type(self, value: DuctType):
        if value is not None:
            self._duct_type = value
        else:
            raise ValueError("duct_type should be of type DuctType")

    @property
    def duct_sub_type(self) -> DuctSubType:
        return self._duct_sub_type

    @duct_sub_type.setter
    def duct_sub_type(self, value: DuctSubType):
        self._duct_sub_type = value

    @property
    def connections(self) -> DuctConnection:
        return self._connections

    @connections.setter
    def connections(self, value: DuctConnection):
        if value is not None:
            self._connections = value
        else:
            raise ValueError("connections should be of type DuctConnection")

    def get_cross_sectional_area(self):
        if self.shape == DuctShape.RECTANGULAR:
            if self.width and self.height:
                return self.height.value * self.width.value
            else:
                raise ValueError('Width and height must be provided for rectangular ducts')
        elif self.shape == DuctShape.ROUND:
            if self.diameter:
                return 3.14159 * (self.diameter.value/2) ** 2
            else:
                raise ValueError('Diameter must be provided for round ducts')

    def get_volume(self):
        if self.length:
            return self.get_cross_sectional_area() * self. length.value
        else:
            raise ValueError('Length must be provided')

    def add_heat_exchanger(self, new_heat_exchanger: HeatExchanger):
        """
        Adds heat exchangers
        :param new_heat_exchanger: a heat exchanger to be added to this duct
        :return:
        """
        EntityInsert.insert_building_entity(self._heat_exchangers, new_heat_exchanger,
                                            BuildingEntity.HVAC_COMPONENT.value)

    def add_filter(self, new_filter: Filter):
        """
        Adds filters to duct
        :param new_filter: a filter to be added to this duct
        :return:
        """
        EntityInsert.insert_building_entity(self._filters, new_filter, BuildingEntity.HVAC_COMPONENT.value)

    def add_anemometer(self, anemometer: Anemometer):
        """
        Adds anemometer to duct
        :param anemometer: an anemometer to be added to this duct
        :return:
        """
        EntityInsert.insert_building_entity(self._anemometers, anemometer, BuildingEntity.HVAC_COMPONENT.value)

    def remove_filter(self, hvac_filter: Filter):
        """
        Removes a filter from a duct
        :param hvac_filter: the filter to remove
        :return:
        """
        EntityRemover.remove_building_entity(self._filters, hvac_filter)

    def get_filters(self, search_terms: Dict = None) -> [Filter]:
        """
        Search filters by attribute values
        :param search_terms: a dictionary of attributes and their values
        :return:
        """
        return StructureEntitySearch.search(self._filters, search_terms)

    def add_fan(self, new_fan: Fan):
        """
        Adds fans
        :param new_fan: a fan to be added to this duct
        :return:
        """
        EntityInsert.insert_building_entity(self._fans, new_fan, BuildingEntity.HVAC_COMPONENT.value)

    def add_connected_air_volume_box(self, new_vav_box: AirVolumeBox):
        """
        Adds VAV boxes connected to this duct
        :param new_vav_box: a fan to be added to this duct
        :return:
        """
        EntityInsert.insert_building_entity(self._connected_air_volume_box, new_vav_box,
                                            BuildingEntity.HVAC_COMPONENT.value)

    def remove_connected_air_volume_box(self, vav_box: AirVolumeBox):
        """
        Removes a VAV box from a duct
        :param vav_box: the VAV box to remove
        :return:
        """
        EntityRemover.remove_building_entity(self._connected_air_volume_box, vav_box)

    def add_damper(self, new_damper: Damper):
        """
        Adds dampers
        :param new_damper: a damper to be added to this duct
        :return:
        """
        EntityInsert.insert_building_entity(self._dampers, new_damper, BuildingEntity.HVAC_COMPONENT.value)

    def remove_fan(self, fan: Fan):
        """
        Removes a fan from a duct
        :param fan: the fan to remove
        :return:
        """
        EntityRemover.remove_building_entity(self._fans, fan)

    def remove_heat_exchanger(self, heat_exchanger: HeatExchanger):
        """
        Removes a heat exchanger from a duct
        :param heat_exchanger: the heat exchanger to remove
        :return:
        """
        EntityRemover.remove_building_entity(self._heat_exchangers, heat_exchanger)

    def remove_damper(self, damper: Damper):
        """
        Removes a damper from a duct
        :param damper: the fan to remove
        :return:
        """
        EntityRemover.remove_building_entity(self._dampers, damper)

    def remove_anemometer(self, anemometer: Anemometer):
        """
        Removes an anemometer from a duct
        :param anemometer: the anemometer to remove
        :return:
        """
        EntityRemover.remove_building_entity(self._anemometers, anemometer)

    def get_heat_exchangers(self, search_terms: Dict = None) -> [HeatExchanger]:
        """
        Search heat exchangers by attribute values
        :param search_terms: a dictionary of attributes and their values
        :return:
        """
        return StructureEntitySearch.search(self._heat_exchangers, search_terms)

    def get_dampers(self, search_terms: Dict = None) -> [Damper]:
        """
        Search dampers by attribute values
        :param search_terms: a dictionary of attributes and their values
        :return:
        """
        return StructureEntitySearch.search(self._dampers, search_terms)

    def get_fans(self, search_terms: Dict = None) -> [Fan]:
        """
        Search fans by attribute values
        :param search_terms: a dictionary of attributes and their values
        :return:
        """
        return StructureEntitySearch.search(self._fans, search_terms)

    def get_anemometers(self, search_terms: Dict = None) -> [Anemometer]:
        """
        Search anemometers by attribute values
        :param search_terms: a dictionary of attributes and their values
        :return:
        """
        return StructureEntitySearch.search(self._anemometers, search_terms)

    def get_connected_air_volume_boxes(self, search_terms: Dict = None) -> [AirVolumeBox]:
        """
        Search air volume boxes by attribute values
        :param search_terms: a dictionary of attributes and their values
        :return:
        """
        return StructureEntitySearch.search(self._connected_air_volume_box, search_terms)

    def __eq__(self, other):
        # ducts are equal if they share the same name
        if isinstance(other, Duct):
            # Check for equality based on the name and UID attribute
            return self.name == other.name and self.UID == other.UID
        return False

    def __str__(self):
        return (
            f"Duct("
            f"UID: {self.UID}, "
            f"name: {self.name}, "
            f"Type: {self.duct_type}, "
            f"SubType: {self.duct_sub_type}, "
            f"Is Insulated: {self._is_insulated}, "
            f"Shape: {self.shape}, "
            f"Length: {self.length}, "
            f"Width: {self.width}, "
            f"Height: {self.height}, "
            f"Diameter: {self.diameter}, "
            f"Fans: {self._fans}, "
            f"Heat Exchangers: {self._heat_exchangers}, "
            f"Dampers: {self._dampers}, "
            f"Air Volume Box: {self._connected_air_volume_box}, "
            f"Filters: {self._filters}, "
            f"Anemometers: {self._anemometers}, "
            f"Connection: {self.connections})"
        )
