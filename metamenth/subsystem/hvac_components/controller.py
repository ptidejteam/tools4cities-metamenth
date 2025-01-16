from metamenth.subsystem.hvac_components.interfaces.abstract_hvac_component import AbstractHVACComponent
from typing import Dict
from metamenth.subsystem.appliance import Appliance
from typing import Union
from metamenth.utils import StructureEntitySearch
from metamenth.utils import EntityRemover
from metamenth.utils import EntityInsert
from metamenth.enumerations import BuildingEntity
from metamenth.datatypes.interfaces.abstract_measure import AbstractMeasure
from metamenth.misc import Validate
from metamenth.controls.abstract_control import AbstractControl
import time

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

    def control(self, control_obj: AbstractControl):
        """
        Executes various control strategies for building systems.
        :param control_obj: The control object is a user implementation of a control strategy for this controller.
        The currently existing contracting are for on/off controls and PID controls. This will be extended to include
        more complex control strategies.
        """
        # Ensure the process value sensor is specified
        if not control_obj.process_value_sensor:
            raise ValueError('Sensor for process variable must be specified')

        # Ensure the process value sensor is part of this controller
        if not self.get_transducer_by_name(control_obj.process_value_sensor.name):
            raise ValueError('The process variable sensor is not configured for this controller')

        if not control_obj.process_actuator:
            raise ValueError('Actuator for process variable must be specified')

        # Ensure the process actuator is part of this controller
        if not self.get_transducer_by_name(control_obj.process_actuator.name):
            raise ValueError('The provided transducer is not configured for this controller')

        # Ensure the data frequency is specified
        if not control_obj.process_value_sensor.data_frequency:
            raise ValueError('Data frequency for the process variable sensor must be specified')

        end_time = time.time() + control_obj.run_duration * 3600 if control_obj.run_duration is not None else None
        # Execute control logic in a loop
        while end_time is None or time.time() < end_time:
            process_value = control_obj.acquire_process_value_data()
            control_obj.execute_control(process_value)
            time.sleep(control_obj.process_value_sensor.data_frequency)


    def __str__(self):
        return (
            f"Controller ({super().__str__()}"
            f"Set Points: {self._set_points}, "
            f"Controlled Entities: {self._controller_entities})"
        )
