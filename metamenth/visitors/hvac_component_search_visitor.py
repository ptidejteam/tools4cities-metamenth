from metamenth.visitors.interfaces.abstract_space_visitor import AbstractSpaceVisitor
from typing import Dict
from metamenth.subsystem.hvac_components.duct import Duct
from metamenth.subsystem.hvac_components.air_volume_box import AirVolumeBox
import itertools


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
                self._add_hvac_component(hvac_component)
            elif isinstance(hvac_component, Duct):
                # check if what we are looking for is inside a duct
                for duct_entity in itertools.chain(
                        hvac_component.get_heat_exchangers(),
                        hvac_component.get_fans(),
                        hvac_component.get_connected_air_volume_boxes(),
                        hvac_component.get_dampers(),
                        hvac_component.get_filters()
                ):
                    if component_class == duct_entity.__class__.__name__:
                        self._add_hvac_component(duct_entity)
            elif isinstance(hvac_component, AirVolumeBox):
                # check if what we are looking for is/are inlet dampers in air volume box
                if hvac_component.inlet_dampers:
                    if hvac_component.inlet_dampers[0].__class__.__name__ == component_class:
                        for damper in hvac_component.inlet_dampers:
                            self._add_hvac_component(damper)

    def _add_hvac_component(self, entity):
        if self._match_criteria(entity, self._hvac_component_criteria):
            self.found_entities.append(entity)
