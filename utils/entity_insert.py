from enumerations import BuildingEntity


class EntityInsert:
    """
    A visitor that remove entities from objects
    """

    def __init__(self):
        pass

    @staticmethod
    def insert_zone(space, zone, building):
        # all unique zones are registered with the building
        if zone not in building.zones:
            building.zones.append(zone)
        if zone not in space.zones:
            # add the space to the zone
            space.zones.append(zone)
            zone.add_spaces([space])

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
        if entity_type == BuildingEntity.TRANSDUCER.value:
            # add transducer to room, open space or subsystem
            EntityInsert._insert_unique(entity_list, entity)

        elif entity_type == BuildingEntity.FLOOR.value:
            # add floor to list of floors in a building
            for floor in entity:
                EntityInsert._insert_unique(entity_list, floor, entity_type)

        elif entity_type in [BuildingEntity.ROOM.value, BuildingEntity.OPEN_SPACE.value]:
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
    def _insert_unique(entity_list, entity, entity_type=None):
        if entity_type == BuildingEntity.FLOOR.value:
            existing_entity = next(
                (new_entity for new_entity in entity_list if new_entity.number == entity.number),
                None
            )
        else:
            existing_entity = next(
                (new_entity for new_entity in entity_list if new_entity.name == entity.name),
                None
            )
        if existing_entity is None:
            entity_list.append(entity)
