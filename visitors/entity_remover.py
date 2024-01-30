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
    def insert_building_entity(building, entity, UID):
        """
        Removes a building entity: floor, meter, weather station and schedule
        :param entity: a string representing the entity (e.g., floor) to remove
        :param UID: the unique ID of the entity to remove
        :param building: the building whose entity is being removed
        :return:
        """
        if entity == BuildingEntity.SCHEDULE.value:
            building.schedules = [schedule for schedule in building.schedules if schedule.UID != UID]
        elif entity == BuildingEntity.METER.value:
            building.meters = [meter for meter in building.meters if meter.UID != UID]
        elif entity == BuildingEntity.FLOOR.value:
            building.floors = [floor for floor in building.floors if floor.UID != UID]
        elif entity == BuildingEntity.WEATHER_STATION.value:
            building.weather_stations = [station for station in building.weather_stations if station.UID != UID]

    @staticmethod
    def remove_floor_entity(floor, entity, UID):
        """
        Removes a floor entity: room,and openspace
        :param entity: a string representing the floor entity to remove
        :param UID: the unique ID of the floor entity
        :param floor, the floor whose entity is being removed
        :return:
        """
        if entity == BuildingEntity.ROOM.value:
            floor.rooms = [room for room in floor.rooms if room.UID != UID]
        elif entity == BuildingEntity.OPEN_SPACE.value:
            floor.open_spaces = [space for space in floor.open_spaces if space.UID != UID]

    @staticmethod
    def remove_space_entity(space, entity, name):
        """
        Removes am entity from a space (room and open spaces)
        :param space: the space (room or open space)
        :param entity: the entity (e.g. transducer, appliance, equipment, etc)
        :param name: the unique name of the entity to be removed
        :return:
        """
        if entity == BuildingEntity.TRANSDUCER.value:
            space.transducers = [transducer for transducer in space.transducers if transducer.name != name]
