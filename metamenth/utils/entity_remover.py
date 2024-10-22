from metamenth.enumerations import BuildingEntity


class EntityRemover:
    """
    A visitor that removes entities into other entities

    Author: Peter Yefi
    Email: peteryefi@gmail.com
    """

    def __init__(self):
        pass

    @staticmethod
    def remove_building_entity(building_entity_list, entity, entity_type=None, entity_object=None):
        """
        Removes a building entity: floor, meter, weather station and schedule
        :param entity: the entity to be removed
        :param entity_type: a string representing the entity (e.g., floor) to remove
        :param building_entity_list: the building whose entity is being removed
        :param entity_object: the object whose list has an item being removed
        :return:
        """

        if entity_type == BuildingEntity.ZONE.value:
            # then remove the zone from the list of zones for the space
            entity.remove_space(entity_object)
            building_entity_list.remove(entity)
        else:
            building_entity_list.remove(entity)

