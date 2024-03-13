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
    def insert_space_entity(space, entity, entity_type):
        """
        Adds an entity to a space
        :param space: the space entity (room or open space) of type AbstractFloorEntity
        :param entity: the entity (e.g. transducers, appliance, equipment, etc)
        :param entity_type: the type of entity
        :return:
        """

        if entity_type == BuildingEntity.TRANSDUCER.value:
            # add tranducer to open space or room
            existing_transducer = next(
                (transducer for transducer in space.transducers if transducer.name == entity.name),
                None
            )

            if existing_transducer is None:
                space.transducers.append(entity)

        elif entity_type == BuildingEntity.SCHEDULE.value:
            if entity not in space.schedules:
                space.schedules.append(entity)

        elif entity_type == BuildingEntity.ZONE.value:
            if entity not in space.zones:
                # add the space to the zone
                entity.add_spaces([space])
                space.zones.append(entity)

        elif entity_type == BuildingEntity.ADJACENT_SPACE.value:
            if entity not in space.adjacent_spaces:
                space.adjacent_spaces.append(entity)

    @staticmethod
    def insert_zonal_entity(zone, entities, entity_type):
        entity_zones = zone.overlapping_zones if entity_type == BuildingEntity.OVERLAPPING_ZONE.value else zone.adjacent_zones
        for new_zone in entities:
            # you can not add the same zone as an adjacent zone
            if zone.name == new_zone.name:
                continue
            # Search for the zone with the same name in the adjacent_zones list
            existing_zone = next(
                (zone for zone in entity_zones if zone.name == new_zone.name),
                None)
            if existing_zone is None:
                # If not found, add the new adjacent zone to the adjacent_zones list
                entity_zones.append(new_zone)

    @staticmethod
    def insert_floor_space(space, entities, entity_type):
        space_entities = space.rooms if entity_type == BuildingEntity.ROOM.value else space.open_spaces
        for space in entities:
            if space not in space_entities:
                space_entities.append(space)

