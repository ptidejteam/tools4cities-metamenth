from enumerations.abstract_enum import AbstractEnum
from typing import Dict


class AbstractSpaceVisitor:
    """
    Defines an interface for visiting
    spaces in buildings
    """

    def __init__(self, zone_criteria: Dict, floor_criteria: Dict,
                 room_criteria: Dict, open_space_criteria: Dict):
        """
        :param zone_criteria: criteria to filter down sensor search to specific zones
        :param floor_criteria: criteria to filter down sensor search to specific floors
        :param room_criteria: criteria to filter down sensor search to specific rooms
        :param open_space_criteria: criteria to filter down sensor search to specific open spaces
        """
        self._zone_criteria = zone_criteria
        self._floor_criteria = floor_criteria
        self._room_criteria = room_criteria
        self._open_space_criteria = open_space_criteria

    def visit_building(self, building):
        print(f'Visiting building: {building.address}')
        for floor in building.get_floors():
            floor.accept(self)

    def visit_zone(self, zone):
        if self._match_criteria(zone, self._zone_criteria):
            print(f'Visiting zone: {zone.name}')
            for space in zone.get_spaces():
                space.accept(self)

    def visit_floor(self, floor):
        if self._match_criteria(floor, self._floor_criteria):
            print(f'Visiting floor: {floor.number}')
        for room in floor.get_rooms():
            room.accept(self)

        for open_space in floor.get_open_spaces():
            open_space.accept(self)

    def visit_room(self, room):
        pass

    def visit_open_space(self, open_space):
        pass

    def _match_criteria(self, entity, criteria):
        """
        Searches for sensors that meet specific criteria
        :param entity: the entity being compare to search criteria
        :param criteria: the filter criteria
        """
        if not criteria:
            return True

        try:
            for key, value in criteria.items():
                att_value = entity.get(key)
                if isinstance(att_value, AbstractEnum):
                    att_value = att_value.value

                if isinstance(value, list):
                    # for list search criteria
                    if att_value not in value:
                        return False
                else:
                    # For single-value criteria
                    if att_value != value:
                        return False
        except AttributeError:
            # handle attribute errors for None types
            pass

        return True
