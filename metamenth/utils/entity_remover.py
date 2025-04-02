"""
Copyright (c) 2023-2025 Peter Yefi.
All rights reserved. This program and the accompanying materials
are made available under the terms of the GNU General Public License v3.0
which accompanies this distribution, and is available at:
https://www.gnu.org/licenses/gpl-3.0.html

Contributors:
    Peter Yefi - API design and implementation
"""

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

