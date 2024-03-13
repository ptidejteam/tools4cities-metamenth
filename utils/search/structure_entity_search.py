from typing import Dict
import sys


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
                    if getattr(entity, attribute) != value:
                        found = False
                if found:
                    results.append(entity)
            except AttributeError as err:
                # TODO: log errors to file
                print(err, file=sys.stderr)

        return results

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
