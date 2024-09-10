from visitors.interfaces.abstract_space_visitor import AbstractSpaceVisitor
from typing import Dict


class SensorSearchVisitor(AbstractSpaceVisitor):
    """
    A concrete visitor that searches for sensors in
    building spaces or zones
    """
    def __init__(self, sensor_criteria: Dict, zone_criteria: Dict = None, floor_criteria: Dict = None,
                 room_criteria: Dict = None, open_space_criteria: Dict = None):
        """
        :param sensor_criteria: the search criteria for sensors
        """
        super().__init__(zone_criteria, floor_criteria, room_criteria, open_space_criteria)
        self._sensor_criteria = sensor_criteria
        self.found_sensors = []

    def visit_room(self, room):
        if self._match_criteria(room, self._room_criteria):
            print(f'Visiting room: {room.name}')
            for sensor in room.get_transducers():
                if self._match_criteria(sensor, self._sensor_criteria):
                    self.found_sensors.append(sensor)

    def visit_open_space(self, open_space):
        if self._match_criteria(open_space, self._open_space_criteria):
            print(f'Visiting open space: {open_space.name}')
            for sensor in open_space.get_transducers():
                if self._match_criteria(sensor, self._sensor_criteria):
                    self.found_sensors.append(sensor)

