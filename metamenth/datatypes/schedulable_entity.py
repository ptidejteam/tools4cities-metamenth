from typing import List
from metamenth.datatypes.operational_schedule import OperationalSchedule
from metamenth.utils import EntityRemover
from metamenth.utils import EntityInsert
from metamenth.utils import StructureEntitySearch
from typing import Dict
from metamenth.enumerations import BuildingEntity


class SchedulableEntity:
    def __init__(self):
        self._schedules: List[OperationalSchedule] = []

    def add_schedule(self, schedule: OperationalSchedule):
        """
        Adds an operational schedule to this building
        :param schedule: the schedule
        :return:
        """
        EntityInsert.insert_building_entity(self._schedules, schedule, BuildingEntity.SCHEDULE.value)
        return self

    def remove_schedule(self, schedule: OperationalSchedule):
        """
        Removes an operational schedule from this building
        :param schedule: the schedule
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

