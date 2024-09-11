from visitors.interfaces.abstract_space_visitor import AbstractSpaceVisitor
from typing import Dict


class MeterSearchVisitor(AbstractSpaceVisitor):
    """
    A concrete visitor that searches for meters in
    building spaces or zones
    """

    def __init__(self, meter_criteria: Dict, zone_criteria: Dict = None, floor_criteria: Dict = None,
                 room_criteria: Dict = None, open_space_criteria: Dict = None):
        """
        :param meter_criteria: the search criteria for meters
        """
        super().__init__(zone_criteria, floor_criteria, room_criteria, open_space_criteria)
        self._meter_criteria = meter_criteria
        self.found_meters = []

    def visit_building(self, building):
        print(f'Visiting building: {building.address}')
        for meter in building.get_meters():
            if self._match_criteria(meter, self._room_criteria):
                self.found_meters.append(meter)

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
                self.found_meters.append(space.meter)

            # search HVAC components in open space for meters
            for hvac_component in space.get_hvac_components():
                if self._match_criteria(hvac_component.meter, self._meter_criteria):
                    if hvac_component.meter:
                        self.found_meters.append(hvac_component.meter)
