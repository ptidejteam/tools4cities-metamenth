from visitors.interfaces.abstract_space_visitor import AbstractSpaceVisitor
from typing import Dict


class HVACComponentSearchVisitor(AbstractSpaceVisitor):
    """
    A concrete visitor that searches for hvac component in
    building spaces
    """

    def __init__(self, hvac_component_criteria: Dict, floor_criteria: Dict = None,
                 room_criteria: Dict = None, open_space_criteria: Dict = None):
        """
        :param hvac_component_criteria: the search criteria for hvac components
        """
        super().__init__(floor_criteria, room_criteria, open_space_criteria)
        if 'component_class' not in hvac_component_criteria:
            raise ValueError(f'hvac component criteria must have component_class value: {hvac_component_criteria}')
        self._hvac_component_criteria = hvac_component_criteria

    def visit_room(self, room):
        if self._match_criteria(room, self._room_criteria):
            print(f'Visiting room: {room.name}')
            self._search_hvac_components(room)

    def visit_open_space(self, open_space):
        if self._match_criteria(open_space, self._open_space_criteria):
            print(f'Visiting open space: {open_space.name}')
            self._search_hvac_components(open_space)

    def _search_hvac_components(self, space):
        component_class = self._hvac_component_criteria['component_class']
        for hvac_component in space.get_hvac_components():
            # check if this hvac component is what we want to search
            if component_class == hvac_component.__class__.__name__:
                # remove component_class attribute and search based on criteria
                del self._hvac_component_criteria['component_class']
                if self._match_criteria(hvac_component, self._hvac_component_criteria):
                    self.found_entities.append(hvac_component)
