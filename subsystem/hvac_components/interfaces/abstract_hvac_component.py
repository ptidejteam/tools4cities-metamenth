from uuid import uuid4
from datatypes.rated_device_measure import RatedDeviceMeasure
from datatypes.operational_schedule import OperationalSchedule
from typing import List
from typing import Dict
from datatypes.continuous_measure import ContinuousMeasure
from measure_instruments.meter import Meter
from utils import StructureEntitySearch
from utils import EntityRemover
from utils import EntityInsert
from datatypes.interfaces.abstract_dynamic_entity import AbstractDynamicEntity


class AbstractHVACComponent(AbstractDynamicEntity):

    def __init__(self, name: str, meter: Meter = None, rated_device_measure: RatedDeviceMeasure = None):
        super().__init__()
        self._UID = str(uuid4())
        self._name = None
        self._meter = meter
        self._rated_device_measure = rated_device_measure
        self._operational_schedule: List[OperationalSchedule] = []
        self._operating_conditions: List[ContinuousMeasure] = []

        self.name = name

    @property
    def UID(self) -> str:
        return self._UID

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        if value is not None:
            self._name = value
        else:
            raise ValueError("name must be of type str")

    @property
    def meter(self) -> Meter:
        return self._meter

    @meter.setter
    def meter(self, value: Meter):
        self._meter = value

    @property
    def rated_device_measure(self) -> RatedDeviceMeasure:
        return self._rated_device_measure

    @rated_device_measure.setter
    def rated_device_measure(self, value: RatedDeviceMeasure):
        self._rated_device_measure = value

    @property
    def operating_conditions(self) -> [ContinuousMeasure]:
        return self._operating_conditions.copy() if self._operating_conditions else []

    @operating_conditions.setter
    def operating_conditions(self, value: [ContinuousMeasure]):
        if value is not None and type(value) is list:
            self._operating_conditions.extend(value)

    @property
    def operational_schedule(self):
        raise AttributeError("Cannot get operational schedules")

    def get_schedule_by_name(self, name) -> OperationalSchedule:
        """
        Search schedules by name
        :param name: the name of the schedule
        :return:
        """
        return StructureEntitySearch.search_by_name(self._operational_schedule, name)

    def get_schedule_by_uid(self, uid) -> OperationalSchedule:
        """
        Search schedule by uid
        :param uid: the unique identifier of the schedule
        :return:
        """
        return StructureEntitySearch.search_by_id(self._operational_schedule, uid)

    def get_schedules(self, search_terms: Dict = None) -> [OperationalSchedule]:
        """
        Search schedules by attributes values
        :param search_terms: a dictionary of attributes and their values
        :return:
        """
        return StructureEntitySearch.search(self._operational_schedule, search_terms)

    def add_schedule(self, schedule: OperationalSchedule):
        """
        Adds an operational schedule to this building
        :param schedule: the schedule
        :return:
        """
        EntityInsert.insert_building_entity(self._operational_schedule, schedule)
        return self

    def remove_schedule(self, schedule: OperationalSchedule):
        """
        Removes an operational schedule from this building
        :param schedule: the schedule
        :return:
        """
        EntityRemover.remove_building_entity(self._operational_schedule, schedule)

    def __eq__(self, other):
        # subsystems are equal if they share the same name
        if isinstance(other, AbstractHVACComponent):
            # Check for equality based on the 'name' attribute
            return self.name == other.name
        return False

    def __str__(self):
        return (
            f"UID: {self.UID}, "
            f"Name: {self.name}, "
            f"Meter: {self.meter}, "
            f"Rated Device Measure: {self.rated_device_measure}, "
            f"Operational Schedule: {self._operational_schedule}, "
            f"Operating Conditions: {self.operating_conditions}, "
        )