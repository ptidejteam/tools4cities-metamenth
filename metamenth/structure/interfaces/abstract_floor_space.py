from typing import List
from metamenth.structure.interfaces.abstract_space import AbstractSpace
from metamenth.datatypes.interfaces.abstract_measure import AbstractMeasure
from metamenth.utils import EntityRemover
from metamenth.utils import EntityInsert
from metamenth.measure_instruments.interfaces.abstract_reader import AbstractReader
from metamenth.utils import StructureEntitySearch
from typing import Dict
from metamenth.datatypes.interfaces.abstract_dynamic_entity import AbstractDynamicEntity
from metamenth.enumerations import BuildingEntity
from metamenth.subsystem.appliance import Appliance
from metamenth.subsystem.hvac_components.interfaces.abstract_hvac_component import AbstractHVACComponent
from metamenth.subsystem.interfaces.abstract_ventilation_component import AbstractVentilationComponent
from metamenth.transducers.interfaces.abstract_transducer import AbstractTransducer
from metamenth.transducers.sensor import Sensor
from metamenth.transducers.actuator import Actuator
from typing import Union
from metamenth.enumerations import SensorMeasure
from metamenth.energysystem.interfaces.abstract_common_energy_system import AbstractCommonEnergySystem
from metamenth.misc import Validate
from metamenth.subsystem.hvac_components.fan import Fan
from metamenth.subsystem.hvac_components.filter import Filter
from metamenth.subsystem.hvac_components.damper import Damper
from metamenth.subsystem.hvac_components.controller import Controller


class AbstractFloorSpace(AbstractSpace, AbstractDynamicEntity):
    """
    An abstract class for spaces on a floor

    Author: Peter Yefi
    Email: peteryefi@gmail.com
    """

    def __init__(self, area: AbstractMeasure, name: str, location: str = None, meter: AbstractReader = None):
        """
        Models spaces on a building's floor
        :param area: the area of the space
        :param name: the name of the space
        :param location: the what3word location of the space
        """
        AbstractSpace.__init__(self, area, location)
        AbstractDynamicEntity.__init__(self)

        self._name = None
        self._adjacent_spaces: List[AbstractFloorSpace] = []
        self._meter = meter
        self._appliances: List[Appliance] = []
        self._hvac_components: Union[List[AbstractHVACComponent], List[AbstractVentilationComponent]] = []
        self._energy_systems: [AbstractCommonEnergySystem] = []
        # apply validation through setters
        self.name = name

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        if value is not None:
            self._name = value
        else:
            raise ValueError("name must be a string")

    @property
    def meter(self) -> AbstractReader:
        return self._meter

    @meter.setter
    def meter(self, value: AbstractReader):
        if value:
            if value.meter_location != self.location:
                raise ValueError("what3words location of meter should be the same as space")
        self._meter = value

    def add_transducer(self, new_transducer: AbstractTransducer):
        """
        Adds sensors and/or actuators to entities (rooms, open spaces, equipment, etc.)
        :param new_transducer: a transducers to be added to this space
        :return:
        """
        if isinstance(new_transducer, Sensor):
            allowed_room_sensors = [SensorMeasure.OCCUPANCY, SensorMeasure.CARBON_DIOXIDE, SensorMeasure.DAYLIGHT,
                                    SensorMeasure.TEMPERATURE, SensorMeasure.HUMIDITY]
            if new_transducer.measure in allowed_room_sensors:
                super().add_transducer(new_transducer)
            else:
                raise ValueError(f'Space sensors must be one of the following: {allowed_room_sensors}')
        elif isinstance(new_transducer, Actuator):
            raise ValueError(f'Actuators cannot be added to rooms directly')

    def add_adjacent_space(self, space: 'AbstractFloorSpace'):
        """
        specifies (adds) which spaces (room and open spaces) are adjacent to other spaces
        :param space:
        :return:
        """
        EntityInsert.insert_building_entity(self._adjacent_spaces, space, BuildingEntity.ADJACENT_SPACE.value)

    def remove_adjacent_space(self, adjacent_space: 'AbstractFloorSpace'):
        """
        Removes adjacent space from a space (room and open space)
        :param adjacent_space: the adjacent space to remove
        :return:
        """
        EntityRemover.remove_building_entity(self._adjacent_spaces, adjacent_space)

    def add_appliance(self, appliance: Appliance):
        """
        adds appliances to floor spaces
        :param appliance: the appliance to add
        :return:
        """
        EntityInsert.insert_building_entity(self._appliances, appliance, BuildingEntity.APPLIANCE.value)

    def remove_appliance(self, appliance: Appliance):
        """
        Removes appliance from a space (room and open space)
        :param appliance: the adjacent space to remove
        :return:
        """
        EntityRemover.remove_building_entity(self._appliances, appliance)

    def add_hvac_component(self, hvac_component: Union[AbstractHVACComponent, AbstractVentilationComponent]):
        """
        adds hvac component to floor spaces
        :param hvac_component: the hvac component to add
        :return:
        """
        if Validate.is_hvac_component_allowed_in_space(hvac_component, [Fan, Damper, Filter, Controller], self):
            EntityInsert.insert_building_entity(self._hvac_components, hvac_component,
                                                BuildingEntity.HVAC_COMPONENT.value)

    def remove_hvac_component(self, hvac_component: Union[AbstractHVACComponent, AbstractVentilationComponent]):
        """
        Removes hvac component from a space (room and open space)
        :param hvac_component: the adjacent space to remove
        :return:
        """
        EntityRemover.remove_building_entity(self._hvac_components, hvac_component)

    def get_hvac_components(self, search_terms: Dict = None) -> Union[List[AbstractHVACComponent],
    List[AbstractVentilationComponent]]:
        """
        Search appliances by attributes values
        :param search_terms: a dictionary of attributes and their values
        :return:
        """
        return StructureEntitySearch.search(self._hvac_components, search_terms)

    def get_adjacent_space_by_name(self, name) -> 'AbstractFloorSpace':
        """
        Search adjacent spaces by name
        :param name: the name of the adjacent space
        :return:
        """
        return StructureEntitySearch.search_by_name(self._adjacent_spaces, name)

    def get_adjacent_space_by_uid(self, uid) -> 'AbstractFloorSpace':
        """
        Search adjacent spaces by uid
        :param uid: the unique identifier of the adjacent spaces
        :return:
        """
        return StructureEntitySearch.search_by_id(self._adjacent_spaces, uid)

    def get_adjacent_spaces(self, search_terms: Dict = None) -> ['AbstractFloorSpace']:
        """
        Search adjacent spaces by attributes values
        :param search_terms: a dictionary of attributes and their values
        :return:
        """
        return StructureEntitySearch.search(self._adjacent_spaces, search_terms)

    def get_appliance_by_name(self, name) -> Appliance:
        """
        Search appliances by name
        :param name: the name of the appliance
        :return:
        """
        return StructureEntitySearch.search_by_name(self._appliances, name)

    def get_appliance_by_uid(self, uid) -> Appliance:
        """
        Search appliance by uid
        :param uid: the unique identifier of the appliance
        :return:
        """
        return StructureEntitySearch.search_by_id(self._appliances, uid)

    def get_appliances(self, search_terms: Dict = None) -> [Appliance]:
        """
        Search appliances by attributes values
        :param search_terms: a dictionary of attributes and their values
        :return:
        """
        return StructureEntitySearch.search(self._appliances, search_terms)

    def add_energy_system(self, energy_system: AbstractCommonEnergySystem):
        """
        adds energy system to floor spaces
        :param energy_system: the energy system to add
        :return:
        """
        EntityInsert.insert_building_entity(self._energy_systems, energy_system, BuildingEntity.HVAC_COMPONENT.value)

    def remove_energy_system(self, energy_system: AbstractCommonEnergySystem):
        """
        Removes energy system from a space (room and open space)
        :param energy_system: the energy system to remove
        :return:
        """
        EntityRemover.remove_building_entity(self._energy_systems, energy_system)

    def get_energy_systems(self, search_terms: Dict = None) -> [AbstractCommonEnergySystem]:
        """
        Search energy systems by attribute values
        :param search_terms: a dictionary of attributes and their values
        :return:
        """
        return StructureEntitySearch.search(self._energy_systems, search_terms)

    def __eq__(self, other):
        # spaces on a floor are equal if they share the same name
        if isinstance(other, AbstractFloorSpace):
            # Check for equality based on the 'name' attribute
            return self.name == other.name
        return False

    def __str__(self) -> str:
        transducers_info = "\n".join([f" - Transducer: {transducer}" for transducer in self._transducers])
        appliances_info = "\n".join([f" - Appliance: {appliance}" for appliance in self._appliances])
        spaces_info = "\n".join([f" - Adjacent Space: {space}" for space in self._adjacent_spaces])
        hvac_component_info = "\n".join([f" - HVAC Components: {component}" for component in self._hvac_components])
        energy_system_info = "\n".join([f" - Energy Systems: {system}" for system in self._energy_systems])

        return (
            f"{super().__str__()}"
            f"Name: {self.name}, "
            f"Meter: {self.meter}, "
            f"Adjacent Spaces: {spaces_info}, "
            f"Transducers: {transducers_info}, "
            f"HVAC Components: {hvac_component_info}, "
            f"Energy Systems: {energy_system_info}, "
            f"Appliances: {appliances_info}\n"
        )
