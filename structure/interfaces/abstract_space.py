import uuid
from datatypes.interfaces.abstract_measure import AbstractMeasure
from misc import Validate
from datatypes.operational_schedule import OperationalSchedule
from typing import List
from enumerations import BuildingEntity
from utils import EntityRemover
from utils import EntityInsert
from utils import StructureEntitySearch
from typing import Dict
from datatypes.interfaces.abstract_zonal_entity import AbstractZonalEntity


class AbstractSpace(AbstractZonalEntity):
    """
    An abstract class for spaces in a building
    """

    def __init__(self, area: AbstractMeasure, location: str = None):
        """
        :param area: The area of the space.
        :param location: The location of the space (three words delimited with two periods).
        """
        super().__init__()
        self._UID = str(uuid.uuid4())
        self._area = None
        self._location = None
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
    def schedules(self):
        raise AttributeError("Cannot get schedules")

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
        EntityInsert.insert_building_entity(self._schedules, schedule, BuildingEntity.SCHEDULE.value)

    def remove_schedule(self, schedule):
        """
        Removes a schedule from a space
        :param schedule: the schedule to remove
        :return:
        """
        EntityRemover.remove_building_entity(self._schedules, schedule)

    def get_schedule_by_name(self, name) -> OperationalSchedule:
        """
        Search schedules by name
        :param name: the name of the schedule
        :return:
        """
        return StructureEntitySearch.search_by_name(self._schedules, name)

    def get_schedule_by_uid(self, uid) -> OperationalSchedule:
        """
        Search schedule by uid
        :param uid: the unique identifier of the schedule
        :return:
        """
        return StructureEntitySearch.search_by_id(self._schedules, uid)

    def get_schedules(self, search_terms: Dict = None) -> [OperationalSchedule]:
        """
        Search schedules by attributes values
        :param search_terms: a dictionary of attributes and their values
        :return:
        """
        return StructureEntitySearch.search(self._schedules, search_terms)

    def __str__(self):
        return (
            f"UID: {self.UID}, "
            f"Area: {self.area}, "
            f"Location: {self.location}, "
            f"Zones: {self._zones}, "
            f"Operational Schedule: {self._schedules}, "
        )
