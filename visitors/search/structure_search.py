from typing import Dict
import sys


class StructureSearch:
    """
    A visitor that search structure from a list of structures
    """

    def __init__(self):
        pass

    @staticmethod
    def search_by_id(structures, uid):
        """
        search structures by unique identifiers
        :param structures: the structures to search: floor, room, open spaces
        :param uid: the unique identifiers
        :return:
        """
        return StructureSearch.search_structure(structures, 'UID', uid)

    @staticmethod
    def search_by_number(structures, entity_number):
        """
        search structures by entity number
        :param structures: the structures to search: floor, room, open spaces
        :param entity_number: the number of the entity
        :return:
        """
        return StructureSearch.search_structure(structures, 'number', entity_number)

    @staticmethod
    def search_by_name(structures, name):
        """
        search structures by name
        :param structures: the structures to search: floor, room, open spaces
        :param name: name of the structure
        :return:
        """
        return StructureSearch.search_structure(structures, 'name', name)

    @staticmethod
    def search(structures, search_terms: Dict):
        """
        search structures based on attribute values
        :param structures: the structures to search: floor, room, open spaces
        :param search_terms: key value pair of attributes and their values
        :return:
        """
        from structure.interfaces.abstract_space import AbstractSpace
        from structure.layer import Layer
        from structure.cover import Cover

        results = []
        for structure in structures:
            if not isinstance(structure, AbstractSpace) and not isinstance(structure, Layer) and \
                not isinstance(structure, Cover):
                raise ValueError('{} is not a structure, layer or cover type'.format(structure))
            found = True
            try:
                for attribute, value in search_terms.items():
                    if getattr(structure, attribute) != value:
                        found = False
                if found:
                    results.append(structure)
            except AttributeError as err:
                # TODO: log errors to file
                print(err, file=sys.stderr)

        return results

    @staticmethod
    def search_structure(structures, search_field, search_value):
        """
        Search for structure floors, rooms, open spaces in a building
        :param structures: the list of structures to search
        :param search_field: the search field of the structure to search
        :param search_value: the value to use in the search
        :return:
        """
        from structure.interfaces.abstract_space import AbstractSpace
        from structure.layer import Layer
        from structure.cover import Cover
        for structure in structures:
            if not isinstance(structure, AbstractSpace) and not isinstance(structure, Layer) and \
                not isinstance(structure, Cover):
                raise ValueError('is not a structure, layer or cover type'.format(structure))
            try:
                if getattr(structure, search_field) == search_value:
                    return structure
            except AttributeError as err:
                # TODO: log errors to file
                print(err, file=sys.stderr)
        return None
