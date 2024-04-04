from uuid import uuid4
from enumerations import DuctType
from enumerations import DuctSubType
from datatypes.interfaces.abstract_dynamic_entity import AbstractDynamicEntity
from datatypes.interfaces.abstract_zonal_entity import AbstractZonalEntity
from subsystem.hvac_components.damper import Damper
from subsystem.hvac_components.fan import Fan
from subsystem.hvac_components.heat_exchanger import HeatExchanger
from typing import List
from subsystem.hvac_components.duct_connection import DuctConnection
from utils import EntityInsert
from utils import EntityRemover
from enumerations import BuildingEntity
from typing import Dict
from utils import StructureEntitySearch


class Duct(AbstractDynamicEntity, AbstractZonalEntity):

    def __init__(self, name: str, duct_type: DuctType):
        AbstractDynamicEntity.__init__(self)
        AbstractZonalEntity.__init__(self)
        self._UID = str(uuid4())
        self._name = None
        self._duct_type = None
        self._duct_sub_type = None
        self._connections = None
        self._heat_exchangers: List[HeatExchanger] = []
        self._fans: List[Fan] = []
        self._dampers: List[Damper] = []

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

    def add_heat_exchanger(self, new_heat_exchanger: HeatExchanger):
        """
        Adds heat exchangers
        :param new_heat_exchanger: a heat exchanger to be added to this duct
        :return:
        """
        EntityInsert.insert_building_entity(self._heat_exchangers, new_heat_exchanger, BuildingEntity.HVAC_COMPONENT.value)

    def add_fan(self, new_fan: Fan):
        """
        Adds fans
        :param new_fan: a fan to be added to this duct
        :return:
        """
        EntityInsert.insert_building_entity(self._fans, new_fan, BuildingEntity.HVAC_COMPONENT.value)

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

    def get_heat_exchangers(self, search_terms: Dict = None):
        """
        Search source entities by attribute values
        :param search_terms: a dictionary of attributes and their values
        :return:
        """
        return StructureEntitySearch.search(self._heat_exchangers, search_terms)

    def get_dampers(self, search_terms: Dict = None):
        """
        Search source entities by attribute values
        :param search_terms: a dictionary of attributes and their values
        :return:
        """
        return StructureEntitySearch.search(self._dampers, search_terms)

    def get_fans(self, search_terms: Dict = None):
        """
        Search source entities by attribute values
        :param search_terms: a dictionary of attributes and their values
        :return:
        """
        return StructureEntitySearch.search(self._fans, search_terms)

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
            f"Fans: {self._fans}, "
            f"Heat Exchangers: {self._heat_exchangers}, "
            f"Dampers: {self._dampers}, "
            f"Connection: {self.connections})"
        )
