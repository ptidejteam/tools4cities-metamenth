from subsystem.hvac_components.interfaces.abstract_hvac_component import AbstractHVACComponent
from typing import Dict
from subsystem.appliance import Appliance
from typing import Union
from utils import StructureEntitySearch
from utils import EntityRemover
from utils import EntityInsert
from enumerations import BuildingEntity
from datatypes.interfaces.abstract_measure import AbstractMeasure
from misc import Validate


class Controller(AbstractHVACComponent):
    def __init__(self, name: str):
        super().__init__(name)
        self._set_points: Dict[str, AbstractMeasure] = {}
        self._controller_entities: [Union[AbstractHVACComponent, Appliance]] = []

    def add_set_point(self, set_point: AbstractMeasure, transducer_pair: tuple):
        """
        Adds a set point for a controller
        :param set_point: the set point to be added
        :param transducer_pair: a tuple indicating the sensor and actuator this set point
        is being added. The formate is (sensor name, actuator name). Note that the sensor and actuator
        must exist before a set point can be added for them
        """
        if len(transducer_pair) != 2:
            raise ValueError('transducer_pair should be a tuple with the format (sensor_name, transducer_name)')

        controller_sensor = self.get_transducer_by_name(transducer_pair[0])
        controller_actuator = self.get_transducer_by_name(transducer_pair[1])
        if controller_sensor and controller_actuator:
            # validate the phenomenon measured by the sensor against the set point
            if set_point:
                if Validate.validate_sensor_type(controller_sensor.measure.value, set_point.measurement_unit.value):
                    self._set_points[f'{transducer_pair[0]}:{transducer_pair[1]}'] = set_point
                else:
                    raise ValueError('Sensor measure: {} not matching set point measure: {}'
                                     .format(controller_sensor.measure,
                                             set_point.measurement_unit))
        else:
            raise ValueError('There is no sensor/actuator found with the provided name for this controller')

    def get_set_point(self, sensor_name: str, actuator_name: str) -> AbstractMeasure:
        """
        Gets a set point
        :param sensor_name: the sensor associated with the set point
        :param actuator_name: the actuator associated with the set point
        """
        return self._set_points.get(f'{sensor_name}:{actuator_name}')

    def remove_set_point(self, sensor_name: str, actuator_name: str):
        """
        Removes a set point
        :param sensor_name: the sensor associated with the set point
        :param actuator_name: the actuator associated with the set point
        """
        if f'{sensor_name}:{actuator_name}' in self._set_points:
            del self._set_points[f'{sensor_name}:{actuator_name}']

    def add_controller_entity(self, entity: Union[AbstractHVACComponent, Appliance]):
        """
        Adds an entity controlled by this controller
        :param entity: the entity that is controlled
        """
        EntityInsert.insert_building_entity(self._controller_entities, entity, BuildingEntity.HVAC_COMPONENT.value)

    def remove_controller_entity(self, entity: Union[AbstractHVACComponent, Appliance]):
        """
        Removes an entity controlled by this controller
        :param entity: the entity to be removed
        """
        EntityRemover.remove_building_entity(self._controller_entities, entity)

    def get_controller_entities(self, search_terms: Dict = None) -> [Union[AbstractHVACComponent, Appliance]]:
        """
        Search data by attributes values
        :param search_terms: a dictionary of attributes and their values
        :return [Union[AbstractHVACComponent, AbstractDuctConnectedComponent, Appliance]]:
        """
        return StructureEntitySearch.search(self._controller_entities, search_terms)

    def __str__(self):
        return (
            f"Controller ({super().__str__()}"
            f"Set Points: {self._set_points}, "
            f"Controlled Entities: {self._controller_entities})"
        )
