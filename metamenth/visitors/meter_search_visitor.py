from metamenth.visitors.interfaces.abstract_space_visitor import AbstractSpaceVisitor
from typing import Dict


class MeterSearchVisitor(AbstractSpaceVisitor):
    """
    A concrete visitor that searches for meters in
    building spaces or zones
    """

    def __init__(self, meter_criteria: Dict, floor_criteria: Dict = None,
                 room_criteria: Dict = None, open_space_criteria: Dict = None):
        """
        :param meter_criteria: the search criteria for meters
        """
        super().__init__(floor_criteria, room_criteria, open_space_criteria)
        self._meter_criteria = meter_criteria

    def visit_building(self, building):
        print(f'Visiting building: {building.address}')
        for meter in building.get_meters():
            if self._match_criteria(meter, self._meter_criteria):
                self.found_entities.append(meter)

        for floor in building.get_floors():
            floor.accept(self)

    def visit_room(self, room):
        if self._match_criteria(room, self._room_criteria):
            print(f'Visiting room: {room.name}')
            self._search_meters(room)

    def visit_open_space(self, open_space):
        if self._match_criteria(open_space, self._open_space_criteria):
            print(f'Visiting open space: {open_space.name}')
            self._search_meters(open_space)

    def _search_meters(self, space):
        if self._match_criteria(space.meter, self._meter_criteria):
            # compare meter in open space to search criteria
            if space.meter:
                self.found_entities.append(space.meter)

            # search HVAC components for meters
            self._search_entities(space.get_hvac_components())
            # search energy systems for meters
            self._search_entities(space.get_energy_systems())

    def _search_entities(self, entities):
        for entity in entities:
            if self._match_criteria(entity.meter, self._meter_criteria):
                if entity.meter:
                    self.found_entities.append(entity.meter)
