from metamenth.subsystem.hvac_components.interfaces.abstract_hvac_component import AbstractHVACComponent
from metamenth.enumerations import DamperType
from metamenth.measure_instruments.damper_position import DamperPosition
from typing import List
from typing import Dict
from metamenth.utils import StructureEntitySearch


class Damper(AbstractHVACComponent):
    def __init__(self, name: str, damper_type: DamperType):
        """
        Models a damper in hvac system
        :param name: the unique name of the heat exchanger
        :param damper_type: the type of damper
        """
        super().__init__(name)
        self._damper_type = None
        self._percentage_opened: [DamperPosition] = []

        self.damper_type = damper_type

    @property
    def damper_type(self) -> DamperType:
        return self._damper_type

    @damper_type.setter
    def damper_type(self, value: DamperType):
        if value is not None:
            self._damper_type = value
        else:
            raise ValueError("damper_type must be of type DamperType")

    def add_damper_position(self, damper_position: DamperPosition):
        return self._percentage_opened.append(damper_position)

    def remove_damper_position(self, damper_position: DamperPosition):
        self._percentage_opened.remove(damper_position)

    def get_damper_positions(self, search_terms: Dict = None) -> List[DamperPosition]:
        """
        Search data by attributes values
        :param search_terms: a dictionary of attributes and their values
        :return [DamperPosition]:
        """
        return StructureEntitySearch.search(self._percentage_opened, search_terms)

    def get_damper_positions_by_date(self, from_timestamp: str, to_timestamp: str = None) -> List[DamperPosition]:
        """
        searches damper positions data based on provided timestamp
        :param from_timestamp: the start timestamp
        :param to_timestamp: the end timestamp
        :return: [DamperPosition]
        """
        return StructureEntitySearch.date_range_search(self._percentage_opened, from_timestamp, to_timestamp)

    def __str__(self):
        return (
            f"Damper ({super().__str__()}"
            f"Type: {self.damper_type}, "
            f"Percentage Opened : {self._percentage_opened})"
        )
