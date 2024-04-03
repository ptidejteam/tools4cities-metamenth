from structure.interfaces.abstract_floor_space import AbstractFloorSpace
from subsystem.hvac_components.interfaces.abstract_hvac_component import AbstractHVACComponent
from enumerations import DuctConnectionEntityType
from subsystem.hvac_components.fan import Fan
from subsystem.hvac_components.heat_exchanger import HeatExchanger
from subsystem.hvac_components.damper import Damper


class DuctConnection:
    def __init__(self):
        self._source_entities = []
        self._destination_entities = []
        self._inside_entities = []
        self._is_loop = False

    def add_entity(self, entity_type: DuctConnectionEntityType, duct_entity):
        """
        Adds an entity to the duct connection
        :param entity_type: the type of duct entity: source, destination, inside
        :param duct_entity: the entity to add
        :return:
        """
        from subsystem.hvac_components.duct import Duct
        allowed_entity_types = [AbstractHVACComponent, AbstractFloorSpace, Duct]
        disallowed_inside_entities = [Fan, Damper, HeatExchanger]

        if any(isinstance(duct_entity, cls) for cls in allowed_entity_types):
            if entity_type == DuctConnectionEntityType.INSIDE:
                if not any(isinstance(duct_entity, cls) for cls in disallowed_inside_entities):
                    self._inside_entities.append(duct_entity)
            elif entity_type == DuctConnectionEntityType.SOURCE:
                if duct_entity not in self._destination_entities:
                    self._source_entities.append(duct_entity)
            elif entity_type == DuctConnectionEntityType.DESTINATION:
                if duct_entity not in self._source_entities:
                    self._destination_entities.append(duct_entity)

