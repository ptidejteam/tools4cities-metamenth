from abc import ABC
import uuid
from datatypes.interfaces.abstract_measure import AbstractMeasure
from misc import Validate
from datatypes.operational_schedule import OperationalSchedule
from typing import List
from enumerations import BuildingEntity
from visitors import EntityRemover
from visitors import EntityInsert


class AbstractSpace(ABC):
    """
    An abstract class for spaces in a building
    """

    def __init__(self, area: AbstractMeasure, location: str = None):
        """
        :param area: The area of the space.
        :param location: The location of the space (three words delimited with two periods).
        """
        self._UID = str(uuid.uuid4())
        self._area = None
        self._location = None
        self._zones = []
        self._schedules: List[OperationalSchedule] = []

        # Apply validation
        self.area = area
        self.location = location

    @property
    def UID(self) -> str:
        return self._UID

    @property
    def area(self) -> AbstractMeasure:
        return self._area

    @area.setter
    def area(self, value: AbstractMeasure):
        if value is None:
            raise ValueError('area must be of type BinaryMeasure')
        self._area = value

    @property
    def location(self) -> str:
        return self._location

    @location.setter
    def location(self, value: str):
        self._location = Validate.validate_what3word(value)

    @property
    def zones(self):
        return self._zones

    @zones.setter
    def zones(self, value):
        if value is not None:
            self._zones = value
        else:
            raise ValueError('zones must be of type [Zone]')

    def add_zone(self, zone, building):
        """
        Adds a zone to this floor
        :param zone: the zone
        :param building, the building which spaces requires a zone
        :return:
        """
        EntityInsert.insert_zone(self, zone, building)

    @property
    def schedules(self) -> List[OperationalSchedule]:
        return self._schedules

    @schedules.setter
    def schedules(self, value: List[OperationalSchedule]):
        if value is not None:
            self._schedules = value
        else:
            raise ValueError('schedule must be of type [OperationalSchedule]')

    def add_schedule(self, schedule: OperationalSchedule):
        """
        Adds a schedule to a space: floor, room or open space
        :param schedule:
        :return:
        """
        EntityInsert.insert_space_entity(self, schedule, BuildingEntity.SCHEDULE.value)

    def remove_schedule(self, name):
        """
        Removes a schedule from a space
        :param name:
        :return:
        """
        EntityRemover.remove_space_entity(self, BuildingEntity.SCHEDULE.value, name)

    def remove_zone(self, zone):
        """
        Removes a zone from a space: floor, room, open space
        :param zone: the zone to be removed
        :return:
        """
        EntityRemover.remove_space_entity(self, BuildingEntity.ZONE.value, zone)

    def __str__(self):
        return (
            f"UID: {self.UID}, "
            f"Area: {self.area}, "
            f"Location: {self.location}, "
            f"Zones: {self.zones}, "
            f"Operational Schedule: {self.schedules}, "
        )
