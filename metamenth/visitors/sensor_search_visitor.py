from metamenth.visitors.interfaces.abstract_space_visitor import AbstractSpaceVisitor
from typing import Dict


class SensorSearchVisitor(AbstractSpaceVisitor):
    """
    A concrete visitor that searches for sensors in
    building spaces or zones
    """
    def __init__(self, sensor_criteria: Dict, floor_criteria: Dict = None,
                 room_criteria: Dict = None, open_space_criteria: Dict = None):
        """
        :param sensor_criteria: the search criteria for sensors
        """
        super().__init__(floor_criteria, room_criteria, open_space_criteria)
        self._sensor_criteria = sensor_criteria

    def visit_room(self, room):
        if self._match_criteria(room, self._room_criteria):
            print(f'Visiting room: {room.name}')
            self._search_sensors(room)

    def visit_open_space(self, open_space):
        if self._match_criteria(open_space, self._open_space_criteria):
            print(f'Visiting open space: {open_space.name}')
            self._search_sensors(open_space)

    def _search_sensors(self, space):
        # search for space sensors
        for sensor in space.get_transducers():
            if self._match_criteria(sensor, self._sensor_criteria):
                self.found_entities.append(sensor)

        # search for HVAC component sensors
        self._search_entities(space.get_hvac_components())
        # search appliances for sensors
        self._search_entities(space.get_appliances())
        # search energy systems for sensors
        self._search_entities(space.get_energy_systems())

    def _search_entities(self, entities):
        for entity in entities:
            for sensor in entity.get_transducers():
                if self._match_criteria(sensor, self._sensor_criteria):
                    self.found_entities.append(sensor)

