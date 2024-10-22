from uuid import uuid4
from metamenth.datatypes.rated_device_measure import RatedDeviceMeasure
from typing import List
from typing import Dict
from metamenth.datatypes.continuous_measure import ContinuousMeasure
from metamenth.measure_instruments.meter import Meter
from metamenth.utils import StructureEntitySearch
from metamenth.utils import EntityRemover
from metamenth.utils import EntityInsert
from metamenth.datatypes.interfaces.abstract_dynamic_entity import AbstractDynamicEntity
from metamenth.enumerations import BuildingEntity
from metamenth.measure_instruments.status_measure import StatusMeasure
from metamenth.datatypes.schedulable_entity import SchedulableEntity


class AbstractHVACComponent(AbstractDynamicEntity):

    def __init__(self, name: str, meter: Meter = None, rated_device_measure: RatedDeviceMeasure = None):
        super().__init__()
        self._UID = str(uuid4())
        self._name = None
        self._meter = meter
        self._rated_device_measure = rated_device_measure
        self._schedulable_entity = SchedulableEntity()
        self._operating_conditions: List[ContinuousMeasure] = []
        self._spaces = []
        self._status_measure: [StatusMeasure] = []

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
    def schedulable_entity(self) -> SchedulableEntity:
        return self._schedulable_entity

    @schedulable_entity.setter
    def schedulable_entity(self, value: SchedulableEntity):
        if value is None:
            raise ValueError("schedules should be of type SchedulableEntity")
        self._schedulable_entity = value

    def add_spaces(self, space: []):
        """
        Adds spaces served by this HVAC component
        :param space: the space
        :return:
        """
        EntityInsert.insert_building_entity(self._spaces, space, BuildingEntity.FLOOR_SPACE.value)
        return self

    def remove_space(self, space):
        """
        Removes a space: floor, room, open space from a hvac component
        :param space: the space to remove
        :return:
        """
        EntityRemover.remove_building_entity(self._spaces, space)

    def get_spaces(self, search_terms: Dict = None) -> []:
        """
        Search spaces served by this component by attributes values
        :param search_terms: a dictionary of attributes and their values
        :return:
        """
        return StructureEntitySearch.search(self._spaces, search_terms)

    def add_status_measure(self, status: StatusMeasure):
        """
        Adds status of hvac component schedule to this building
        :param status: the schedule
        :return:
        """
        EntityInsert.insert_building_entity(self._status_measure, status)
        return self

    def remove_status_measure(self, status):
        """
        Removes a status measure from a hvac component
        :param status: the status measure to remove
        :return:
        """
        EntityRemover.remove_building_entity(self._status_measure, status)

    def get_status_measure(self, search_terms: Dict = None) -> [StatusMeasure]:
        """
        Search data by attributes values
        :param search_terms: a dictionary of attributes and their values
        :return [StatusMeasure]:
        """
        return StructureEntitySearch.search(self._status_measure, search_terms)

    def get_status_measure_by_date(self, from_timestamp: str, to_timestamp: str = None) -> [StatusMeasure]:
        """
        searches status data based on provided timestamp
        :param from_timestamp: the start timestamp
        :param to_timestamp: the end timestamp
        :return: [StatusMeasure]
        """
        return StructureEntitySearch.date_range_search(self._status_measure, from_timestamp, to_timestamp)

    def __eq__(self, other):
        # subsystems are equal if they share the same name
        if isinstance(other, AbstractHVACComponent):
            # Check for equality based on the 'name' attribute
            return self.name == other.name
        return False

    def get(self, attribute):
        return getattr(self, attribute, None)

    def __str__(self):
        return (
            f"UID: {self.UID}, "
            f"Name: {self.name}, "
            f"Meter: {self.meter}, "
            f"Rated Device Measure: {self.rated_device_measure}, "
            f"Operational Schedule: {self._schedulable_entity}, "
            f"Operating Conditions: {self.operating_conditions}, "
        )