from abc import ABC
from metamenth.utils import EntityInsert
from metamenth.utils import EntityRemover
from metamenth.utils import StructureEntitySearch
from metamenth.transducers.interfaces.abstract_transducer import AbstractTransducer
from metamenth.enumerations import BuildingEntity
from typing import Dict


class AbstractDynamicEntity(ABC):

    def __init__(self):
        self._transducers: [AbstractTransducer] = []

    @property
    def transducers(self) -> [AbstractTransducer]:
        return self._transducers.copy()

    def add_transducer(self, new_transducer: AbstractTransducer):
        """
        Adds sensors and/or actuators to entities (rooms, open spaces, equipment, etc.)
        :param new_transducer: a transducers to be added to this space
        :return:
        """
        EntityInsert.insert_building_entity(self._transducers, new_transducer, BuildingEntity.TRANSDUCER.value)

    def remove_transducer(self, transducer: AbstractTransducer):
        """
        Removes a transducers from a subsystem
        :param transducer: the transducers to remove
        :return:
        """
        EntityRemover.remove_building_entity(self._transducers, transducer)

    def get_transducer_by_name(self, name) -> AbstractTransducer:
        """
        Search transducer by name
        :param name:  the name of the transducer
        :return:
        """
        return StructureEntitySearch.search_by_name(self._transducers, name)

    def get_transducer_by_uid(self, uid) -> AbstractTransducer:
        """
        Search transducers by uid
        :param uid: the unique identifier of the transducer
        :return:
        """
        return StructureEntitySearch.search_by_id(self._transducers, uid)

    def get_transducers(self, search_terms: Dict = None) -> ['AbstractTransducer']:
        """
        Search transducers by attributes values
        :param search_terms: a dictionary of attributes and their values
        :return:
        """
        return StructureEntitySearch.search(self._transducers, search_terms)