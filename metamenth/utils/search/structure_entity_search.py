from typing import Dict
import sys
from datetime import datetime
from typing import Union
from typing import List
from metamenth.measure_instruments.sensor_data import SensorData
from metamenth.measure_instruments.trigger_history import TriggerHistory
from metamenth.measure_instruments.meter_measure import MeterMeasure
from metamenth.measure_instruments.weather_data import WeatherData
from metamenth.misc import Validate
from metamenth.enumerations.abstract_enum import AbstractEnum


class StructureEntitySearch:
    """
    A visitor that entities in structures, e.g., meter, weather, stations, etc
    """

    def __init__(self):
        pass

    @staticmethod
    def search_by_id(entity_list, uid):
        """
        search structures by unique identifiers
        :param entity_list: the list of entity to search for a particular entity
        :param uid: the unique identifiers
        :return:
        """
        return StructureEntitySearch.search_structure_entity(entity_list, 'UID', uid)

    @staticmethod
    def search_by_name(entity_list, name):
        """
        search structures by name
        :param entity_list: the list of entity to search for a particular entity
        :param name: name of the structure
        :return:
        """
        return StructureEntitySearch.search_structure_entity(entity_list, 'name', name)

    @staticmethod
    def search(entity_list, search_terms: Dict):
        """
        search entities based on attribute values
        :param entity_list: the list of entity to search for a particular entity
        :param search_terms: key value pair of attributes and their values
        :return:
        """
        results = []
        if search_terms is None:
            return entity_list

        for entity in entity_list:
            found = True
            try:
                for attribute, value in search_terms.items():
                    att_value = getattr(entity, attribute)
                    if isinstance(att_value, AbstractEnum):
                        att_value = att_value.value
                    if att_value != value:
                        found = False
                if found:
                    results.append(entity)
            except AttributeError as err:
                # TODO: log errors to file
                print(err, file=sys.stderr)

        return results

    @staticmethod
    def date_range_search(entity_list: Union[List[SensorData], List[TriggerHistory], List[MeterMeasure],
                                             List[WeatherData]], from_timestamp: str, to_timestamp: str = None):
        """

        :param entity_list: a list of sensor, actuator or meter data
        :param from_timestamp: the start timestamp
        :param to_timestamp: the end timestamp
        :return:
        """
        if len(from_timestamp) == 10:  # Check if only date is provided
            from_timestamp += ' 00:00:00'  # Add default time of midnight

        if to_timestamp is None:
            to_tp = datetime.now().replace(microsecond=0)
        else:
            if len(to_timestamp) == 10:  # Check if only date is provided
                to_timestamp += ' 23:59:59'
            to_tp = Validate.parse_date(to_timestamp)
        from_tp = Validate.parse_date(from_timestamp)
        filtered_data = []
        for data in entity_list:
            if from_tp <= data.timestamp <= to_tp:
                filtered_data.append(data)

        return filtered_data

    @staticmethod
    def search_structure_entity(entity_list, search_field, search_value):
        """
        Search for structure floors, rooms, open spaces in a building
        :param entity_list: the list of entities to search
        :param search_field: the search field
        :param search_value: the search value
        :return:
        """

        for entity in entity_list:
            try:
                if getattr(entity, search_field) == search_value:
                    return entity
            except AttributeError as err:
                # TODO: log errors to file
                print(err, file=sys.stderr)
        return None
