from metamenth.visitors.interfaces.abstract_space_visitor import AbstractSpaceVisitor
from typing import Dict


class SpaceSearchVisitor(AbstractSpaceVisitor):
    """
    A concrete visitor that searches for sensors in
    building spaces or zones
    """

    def __init__(self, floor_criteria: Dict = None,
                 room_criteria: Dict = None, open_space_criteria: Dict = None, include_floor: bool = True):
        super().__init__(floor_criteria, room_criteria, open_space_criteria)
        self._include_floor = include_floor

    def visit_floor(self, floor):
        """
        override visit floor from AbstractSpace Visitor
        """
        if self._match_criteria(floor, self._floor_criteria):
            print(f'Visiting floor: {floor.number}')
            if self._include_floor:
                self.found_entities.append(floor)

            for room in floor.get_rooms():
                room.accept(self)

            for open_space in floor.get_open_spaces():
                open_space.accept(self)

    def visit_room(self, room):
        if self._match_criteria(room, self._room_criteria):
            self.found_entities.append(room)

    def visit_open_space(self, open_space):
        if self._match_criteria(open_space, self._open_space_criteria):
            self.found_entities.append(open_space)
