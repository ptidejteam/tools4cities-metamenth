from visitors.interfaces.space_visitor import AbstractSpaceVisitor
from enumerations.abstract_enum import AbstractEnum


class SensorSearchVisitor(AbstractSpaceVisitor):
    """
    A concrete visitor that searches for sensors in
    building spaces or zones
    """
    def __init__(self, sensor_criteria):
        self._sensor_criteria = sensor_criteria
        self.found_sensors = []

    def visit_building(self, building):
        print(f'Visiting building: {building.address}')
        for floor in building.get_floors():
            floor.accept(self)

    def visit_zone(self, zone):
        print(f'Visiting zone: {zone.name}')
        for space in zone.get_spaces():
            space.accept(self)

    def visit_floor(self, floor):
        print(f'Visiting floor: {floor.number}')
        for room in floor.get_rooms():
            room.accept(self)

        for open_space in floor.get_open_spaces():
            open_space.accept(self)

    def visit_room(self, room):
        print(f'Visiting room: {room.name}')
        for sensor in room.get_transducers():
            if self._match_criteria(sensor):
                self.found_sensors.append(sensor)

    def visit_open_space(self, open_space):
        print(f'Visiting open space: {open_space.name}')
        for sensor in open_space.get_transducers():
            if self._match_criteria(sensor):
                self.found_sensors.append(sensor)

    def _match_criteria(self, sensor):
        """
        Searches for sensors that meet specific criteria
        :param sensor: the sensor being compare to search criteria
        """
        for key, value in self._sensor_criteria.items():
            att_value = sensor.get(key)
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
        return True
