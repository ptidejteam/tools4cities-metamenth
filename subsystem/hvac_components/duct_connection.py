from structure.interfaces.abstract_space import AbstractSpace
from subsystem.hvac_components.interfaces.abstract_hvac_component import AbstractHVACComponent
from enumerations import DuctConnectionEntityType
from subsystem.hvac_components.circulation_pump import CirculationPump
from subsystem.hvac_components.compressor import Compressor
from subsystem.hvac_components.pump import Pump
from subsystem.hvac_components.heat_pump import HeatPump
from subsystem.hvac_components.condenser import Condenser
from subsystem.hvac_components.heat_exchanger import HeatExchanger
from subsystem.hvac_components.air_volume_box import AirVolumeBox
from subsystem.hvac_components.cooling_tower import CoolingTower
from subsystem.hvac_components.chiller import Chiller
from subsystem.hvac_components.boiler import Boiler
from utils import StructureEntitySearch
from typing import Dict


class DuctConnection:
    def __init__(self):
        self._source_entities = []
        self._destination_entities = []
        self._is_loop = False

    def add_entity(self, entity_type: DuctConnectionEntityType, duct_entity):
        """
        Adds an entity to the duct connection
        :param entity_type: the type of duct entity: source, destination, inside
        :param duct_entity: the entity to add
        :return:
        """
        from subsystem.hvac_components.duct import Duct
        allowed_entity_types = [HeatExchanger, AbstractSpace, Duct, Boiler, Chiller, CirculationPump,
                                Compressor, Pump, HeatPump, Condenser, AirVolumeBox, CoolingTower]

        if any(isinstance(duct_entity, cls) for cls in allowed_entity_types):
            if entity_type == DuctConnectionEntityType.SOURCE:
                if duct_entity not in self._destination_entities:
                    self._source_entities.append(duct_entity)
            elif entity_type == DuctConnectionEntityType.DESTINATION:
                if duct_entity not in self._source_entities:
                    self._destination_entities.append(duct_entity)
        else:
            raise ValueError(f'{duct_entity} cannot be connected to a duct')

    def remove_entity(self, entity_type: DuctConnectionEntityType, duct_entity):
        """
        Removes an entity from the duct connection
        :param entity_type: the type of duct entity: source, destination, inside
        :param duct_entity: the entity to add
        :return:
        """
        if entity_type == DuctConnectionEntityType.SOURCE:
            if duct_entity in self._source_entities:
                self._source_entities.remove(duct_entity)
        elif entity_type == DuctConnectionEntityType.DESTINATION:
            if duct_entity in self._destination_entities:
                self._destination_entities.remove(duct_entity)

    def get_source_entities(self, search_terms: Dict = None):
        """
        Search source entities by attribute values
        :param search_terms: a dictionary of attributes and their values
        :return:
        """
        return StructureEntitySearch.search(self._source_entities, search_terms)

    def get_destination_entities(self, search_terms: Dict = None):
        """
        Search destination entities by attribute values
        :param search_terms: a dictionary of attributes and their values
        :return:
        """
        return StructureEntitySearch.search(self._destination_entities, search_terms)

    @property
    def is_loop(self) -> bool:
        return self._is_loop

    @is_loop.setter
    def is_loop(self, value: bool):
        if value:
            if len(self._source_entities) <= 1 and len(self._destination_entities) <= 1:
                self._is_loop = value
            else:
                raise ValueError("is_loop can only be true if there are single source and destination entities")
        else:
            self._is_loop = value

    def __str__(self):
        return (
            f"DuctConnection ({super().__str__()}"
            f"Source Entities: {self._source_entities}, "
            f"Destination Entities: {self._destination_entities}, "
            f"Is Loop: {self._is_loop})"
        )

