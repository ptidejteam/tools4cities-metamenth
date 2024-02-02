from enumerations import BuildingEntity


class EntityRemover:
    """
    A visitor that removes entities into other entities

    Author: Peter Yefi
    Email: peteryefi@gmail.com
    """

    def __init__(self):
        pass

    @staticmethod
    def remove_building_entity(building, entity_type, entity):
        """
        Removes a building entity: floor, meter, weather station and schedule
        :param entity: the entity to be removed
        :param entity_type: a string representing the entity (e.g., floor) to remove
        :param building: the building whose entity is being removed
        :return:
        """
        if entity_type == BuildingEntity.SCHEDULE.value:
            building.schedules.remove(entity)
        elif entity_type == BuildingEntity.METER.value:
            building.meters.remove(entity)
        elif entity_type == BuildingEntity.FLOOR.value:
            building.floors.remove(entity)
        elif entity_type == BuildingEntity.WEATHER_STATION.value:
            building.weather_stations.remove(entity)

    @staticmethod
    def remove_floor_entity(floor, entity_type, entity):
        """
        Removes a floor entity: room,and openspace
        :param entity_type: a string representing the floor entity to remove
        :param entity: the floor entity to be removed
        :param floor, the floor whose entity is being removed
        :return:
        """
        if entity_type == BuildingEntity.ROOM.value:
            floor.rooms.remove(entity)
        elif entity_type == BuildingEntity.OPEN_SPACE.value:
            floor.open_spaces.remove(entity)

    @staticmethod
    def remove_space_entity(space, entity_type, entity):
        """
        Removes am entity from a space (room and open spaces)
        :param space: the space (room or open space)
        :param entity: the entity (e.g. transducers, appliance, equipment, etc)
        :param entity_type: the type of entity
        :return:
        """
        if entity_type == BuildingEntity.TRANSDUCER.value:
            space.transducers.remove(entity)
        elif entity_type == BuildingEntity.SCHEDULE.value:
            space.schedules.remove(entity)
        elif entity_type == BuildingEntity.ZONE.value:
            # remove the space from the zone
            entity.remove_space(space)
            # then remove the zone from the list of zones for the space
            space.zones.remove(entity)
        elif entity_type == BuildingEntity.ADJACENT_SPACE.value:
            space.adjacent_spaces.remove(entity)

    @staticmethod
    def remove_zonal_entity(zone, entity_type, entity):
        """
        Removes a zonal entity
        :param entity_type: a string representing the floor entity to remove
        :param entity: the zonal entity to remove
        :param zone: the zone whose entity is being removed
        :return:
        """
        if entity_type == BuildingEntity.SPACE.value:
            zone.spaces.remove(entity)
        elif entity_type == BuildingEntity.ADJACENT_ZONE.value:
            zone.adjacent_zones.remove(entity)
        elif entity_type == BuildingEntity.OVERLAPPING_ZONE.value:
            zone.overlapping_zones.remove(entity)
