from uuid import uuid4
from metamenth.enumerations import VentilationType
from metamenth.subsystem.hvac_components.duct import Duct
from metamenth.subsystem.interfaces.abstract_ventilation_component import AbstractVentilationComponent
from metamenth.utils import EntityRemover
from metamenth.utils import EntityInsert
from metamenth.utils import StructureEntitySearch
from typing import Dict
from typing import Union
from metamenth.energysystem.engine import Engine
from typing import List


class VentilationSystem:
    def __init__(self, ventilation_type: VentilationType, principal_duct: Duct):
        """
        Models ventilation system in a building
        :param ventilation_type: the type of ventilation
        :param principal_duct: the principal duct of the ventilation system
        """
        self._UID = str(uuid4())
        self._ventilation_type = None
        self._principal_duct = None
        self._components: [Union[AbstractVentilationComponent, Engine]] = []

        self.ventilation_type = ventilation_type
        self.principal_duct = principal_duct

    @property
    def UID(self) -> str:
        return self._UID

    @property
    def ventilation_type(self) -> VentilationType:
        return self._ventilation_type

    @ventilation_type.setter
    def ventilation_type(self, value: VentilationType):
        if value is not None:
            self._ventilation_type = value
        else:
            raise ValueError("ventilation_type should be of type VentilationType")

    @property
    def principal_duct(self) -> Duct:
        return self._principal_duct

    @principal_duct.setter
    def principal_duct(self, value: Duct):
        if value is not None:
            self._principal_duct = value
        else:
            raise ValueError("principal_duct should be of type Duct")

    def get_components(self, search_terms: Dict = None) -> Union[List[AbstractVentilationComponent], List[Engine]]:
        """
        Search ventilation components by attributes values
        :param search_terms: a dictionary of attributes and their values
        :return:
        """
        return StructureEntitySearch.search(self._components, search_terms)

    def add_component(self, component: Union[AbstractVentilationComponent, Engine]):
        """
        Adds a ventilation component to the ventilation system
        :param component: the component to add
        :return:
        """
        EntityInsert.insert_building_entity(self._components, component)
        return self

    def remove_component(self, component: Union[AbstractVentilationComponent, Engine]):
        """
        Removes a ventilation component from the ventilation system
        :param component: the component to remove
        :return:
        """
        EntityRemover.remove_building_entity(self._components, component)

    def __eq__(self, other):
        # ventilation systems are equal if they share the same UID
        if isinstance(other, Duct):
            # Check for equality based on the UID attribute
            return self.UID == other.UID
        return False

    def __str__(self):
        return (
            f"VentilationSystem("
            f"UID: {self.UID}, "
            f"Type: {self.ventilation_type}, "
            f"Principal Duct: {self.principal_duct}"
            f"Components: {self._components})"
        )