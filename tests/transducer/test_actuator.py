from unittest import TestCase
from misc import MeasureFactory
from enumerations import RecordingType
from datatypes.measure import Measure
from enumerations import MeasurementUnit
from transducers.sensor import Sensor
from enumerations import SensorMeasure
from enumerations import SensorMeasureType
from transducers.actuator import Actuator
from measure_instruments.trigger_history import TriggerHistory
from enumerations import TriggerType
from subsystem.hvac_components.damper import Damper
from subsystem.hvac_components.fan import Fan
from subsystem.hvac_components.variable_frequency_drive import VariableFrequencyDrive
from enumerations import DamperType
from enumerations import PowerState
from subsystem.hvac_components.controller import Controller


class TestActuator(TestCase):

    def setUp(self) -> None:
        self.temp_set_point = MeasureFactory.create_measure(RecordingType.CONTINUOUS.value,
                                                            Measure(MeasurementUnit.DEGREE_CELSIUS, 10, 20))
        self.damper = Damper("PR.VNT.DP.01", DamperType.BACK_DRAFT)

    def test_damper_actuator(self):
        actuator = Actuator("DAMPER.ACT", self.damper)
        self.assertEqual(actuator.name, "DAMPER.ACT")
        self.assertIsNotNone(actuator.UID)
        self.assertEqual(actuator.trigger_output, self.damper)

    def test_actuator_with_continuous_set_point(self):
        vfd = VariableFrequencyDrive('PR.VNT.VRD.01')
        fan = Fan("PR.VNT.FN.01", PowerState.ON, vfd)
        actuator = Actuator("FAN.ACT", fan)
        self.assertEqual(actuator.name, "FAN.ACT")
        self.assertIsNotNone(actuator.UID)
        self.assertEqual(actuator.trigger_output, fan)

    def test_actuator_with_controller(self):
        controller = Controller('CTR')
        actuator = Actuator("DAMPER.ACT", self.damper)
        actuator.controller = controller
        self.assertIsNotNone(actuator.UID)
        self.assertEqual(actuator.controller, controller)

    def test_actuator_with_set_points_without_controller_transducers(self):
        controller = Controller('CTR')
        temperature_set_point = MeasureFactory.create_measure(RecordingType.CONTINUOUS.value,
                                                              Measure(MeasurementUnit.DEGREE_CELSIUS, 10, 20))
        temp_sensor = Sensor("TEMP.SENSOR", SensorMeasure.TEMPERATURE, MeasurementUnit.DEGREE_CELSIUS,
                             SensorMeasureType.THERMO_COUPLE_TYPE_B, 10)
        actuator = Actuator("DAMPER.ACT", self.damper)
        try:
            controller.add_set_point(temperature_set_point, (temp_sensor.name, actuator.name))
        except ValueError as err:
            self.assertEqual(err.__str__(), 'There is no sensor/actuator found with the provided name for this '
                                            'controller')

    def test_actuator_with_set_points(self):
        controller = Controller('CTR')
        temperature_set_point = MeasureFactory.create_measure(RecordingType.CONTINUOUS.value,
                                                              Measure(MeasurementUnit.DEGREE_CELSIUS, 10, 20))
        temp_sensor = Sensor("TEMP.SENSOR", SensorMeasure.TEMPERATURE, MeasurementUnit.DEGREE_CELSIUS,
                             SensorMeasureType.THERMO_COUPLE_TYPE_B, 10)
        actuator = Actuator("DAMPER.ACT", self.damper)
        controller.add_transducer(temp_sensor)
        controller.add_transducer(actuator)
        controller.add_set_point(temperature_set_point, (temp_sensor.name, actuator.name))
        actuator.controller = controller

        self.assertIsNotNone(actuator.UID)
        self.assertEqual(actuator.controller, controller)
        self.assertEqual(actuator.controller.get_set_point(temp_sensor.name, actuator.name), temperature_set_point)

    def test_actuator_sensor_input_with_mismatch_set_point(self):
        try:
            controller = Controller('CTR')
            temperature_set_point = MeasureFactory.create_measure(RecordingType.CONTINUOUS.value,
                                                                  Measure(MeasurementUnit.DEGREE_CELSIUS, 10, 20))
            pressure_sensor = Sensor("PR.SENSOR", SensorMeasure.PRESSURE, MeasurementUnit.PASCAL,
                                     SensorMeasureType.THERMO_COUPLE_TYPE_B, 10)
            actuator = Actuator("DAMPER.ACT", self.damper)
            controller.add_transducer(pressure_sensor)
            controller.add_transducer(actuator)
            controller.add_set_point(temperature_set_point, (pressure_sensor.name, actuator.name))
            actuator.controller = controller
        except ValueError as err:
            self.assertEqual(err.__str__(),
                             "Sensor measure: SensorMeasure.PRESSURE not matching set point measure: "
                             "MeasurementUnit.DEGREE_CELSIUS")

    def test_actuator_with_metadata_and_registry_id(self):
        actuator = Actuator("DAMPER.ACT", self.damper)
        meta_data = {
            'description': 'Opens a valve when temperature value exceeds 20oC'
        }
        actuator.meta_data = meta_data
        actuator.registry_id = 'UID.VALVE.023'
        self.assertEqual(actuator.meta_data, meta_data)
        self.assertEqual(actuator.meta_data['description'], 'Opens a valve when temperature value exceeds 20oC')
        self.assertEqual(actuator.registry_id, 'UID.VALVE.023')

    def test_actuator_with_input_voltage_range(self):
        damper = Damper("PR.VNT.DP.01", DamperType.BACK_DRAFT)
        actuator = Actuator("FILTER.ACT", damper)
        input_voltage_range = MeasureFactory.create_measure(RecordingType.CONTINUOUS.value,
                                                            Measure(MeasurementUnit.VOLT, 0.5, 0.8))
        actuator.input_voltage_range = input_voltage_range
        self.assertEqual(actuator.input_voltage_range, input_voltage_range)
        self.assertEqual(actuator.output_voltage_range, None)

    def test_add_data_to_actuator(self):
        actuator = Actuator("FILTER.ACT", self.damper)
        trigger_his = TriggerHistory(TriggerType.CLOSE)
        actuator.add_data([trigger_his])
        self.assertEqual(actuator.get_data(), [trigger_his])
        self.assertEqual(actuator.get_data()[0].trigger_type, trigger_his.trigger_type.CLOSE)
        self.assertIsNotNone(actuator.get_data()[0].timestamp)

    def test_remove_data_from_actuator(self):
        actuator = Actuator("FILTER.ACT", self.damper)
        trigger_his = TriggerHistory(TriggerType.OPEN_CLOSE, 1)
        actuator.add_data([trigger_his])
        self.assertEqual(actuator.get_data(), [trigger_his])

        actuator.remove_data(trigger_his)
        self.assertEqual(actuator.get_data(), [])
        self.assertEqual(len(actuator.get_data()), 0)
