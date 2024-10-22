from metamenth.enumerations import BuildingEntity


class EntityInsert:
    """
    A visitor that remove entities from objects
    """

    def __init__(self):
        pass

    @staticmethod
    def insert_zone(entity, zone, building):
        # all unique zones are registered with the building
        if zone not in building.zones:
            building.zones.append(zone)
        if zone not in entity.zones:
            # add the space to the zone
            entity.zones.append(zone)
            from metamenth.structure.interfaces.abstract_space import AbstractSpace
            if isinstance(entity, AbstractSpace):
                zone.add_spaces([entity])

    @staticmethod
    def insert_building_entity(entity_list, entity, entity_type=None, entity_object=None):
        """
        Adds an entity to a space
        :param entity_list: the list of entity to add to (e.g., list of rooms or open space)
        :param entity: the entity (e.g. transducers, appliance, equipment, etc)
        :param entity_type: the type of entity
        :param entity_object: the entity object
        :return:
        """
        if entity_type in [BuildingEntity.TRANSDUCER.value, BuildingEntity.SCHEDULE.value,
                           BuildingEntity.ADJACENT_SPACE.value, BuildingEntity.APPLIANCE.value,
                           BuildingEntity.HVAC_COMPONENT.value, BuildingEntity.FLOOR.value]:
            # add transducer to room, open space or subsystem
            EntityInsert._insert_unique(entity_list, entity)

        elif entity_type == BuildingEntity.FLOOR_SPACE.value:
            # add open space or room to list of rooms

            for space in entity:
                EntityInsert._insert_unique(entity_list, space)

        elif entity_type == BuildingEntity.ZONE.value:
            if entity not in entity_list:
                # add the space to the zone
                entity.add_spaces([entity_object])
                entity_list.append(entity)

        elif entity_type in [BuildingEntity.OVERLAPPING_ZONE.value, BuildingEntity.ADJACENT_ZONE.value]:
            for new_zone in entity:
                # you can not add the same zone as an adjacent zone
                if entity_object == new_zone:
                    continue
                EntityInsert._insert_unique(entity_list, new_zone)
        else:
            entity_list.append(entity)

    @staticmethod
    def _insert_unique(entity_list, entity):
        if not entity in entity_list:
            entity_list.append(entity)
