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


class TestSensor(TestCase):

    def setUp(self) -> None:
        self.temp_set_point = MeasureFactory.create_measure(RecordingType.CONTINUOUS.value,
                                                            Measure(MeasurementUnit.DEGREE_CELSIUS, 10, 20))

    def test_damper_actuator(self):
        # TODO: Replace object with damper after implementation of damper class
        actuator = Actuator("DAMPER.ACT", object())
        self.assertEqual(actuator.name, "DAMPER.ACT")
        self.assertIsNotNone(actuator.UID)
        self.assertEqual(actuator.set_point, None)

    def test_actuator_with_continuous_set_point(self):
        actuator = Actuator("FILTER.ACT", object())
        actuator.set_point = self.temp_set_point
        self.assertEqual(actuator.name, "FILTER.ACT")
        self.assertIsNotNone(actuator.UID)
        self.assertEqual(actuator.set_point, self.temp_set_point)

    def test_actuator_with_sensor_input(self):
        actuator = Actuator("FILTER.ACT", object())
        actuator.set_point = self.temp_set_point

        temp_sensor = Sensor("TEMP.SENSOR", SensorMeasure.TEMPERATURE, MeasurementUnit.DEGREE_CELSIUS,
                             SensorMeasureType.THERMO_COUPLE_TYPE_B, 10)
        actuator.trigger_input = temp_sensor
        self.assertEqual(actuator.name, "FILTER.ACT")
        self.assertIsNotNone(actuator.UID)
        self.assertEqual(actuator.set_point, self.temp_set_point)
        self.assertEqual(actuator.trigger_input, temp_sensor)
        self.assertEqual(actuator.trigger_input.data_frequency, 10)

    def test_actuator_sensor_input_with_mismatch_set_point(self):
        try:
            actuator = Actuator("FILTER.ACT", object())
            actuator.set_point = self.temp_set_point

            pressure_sensor = Sensor("PRESSURE.SENSOR", SensorMeasure.PRESSURE, MeasurementUnit.PASCAL,
                                     SensorMeasureType.THERMO_COUPLE_TYPE_B, 10)
            actuator.trigger_input = pressure_sensor
            self.assertEqual(actuator.name, "FILTER.ACT")
            self.assertIsNotNone(actuator.UID)
            self.assertEqual(actuator.set_point, self.temp_set_point)
            self.assertEqual(actuator.trigger_input, pressure_sensor)
            self.assertEqual(actuator.trigger_input.data_frequency, 10)
        except ValueError as err:
            self.assertEqual(err.__str__(),
                             "Input sensor measure: MeasurementUnit.PASCAL not matching set point measure: "
                             "MeasurementUnit.DEGREE_CELSIUS")

    def test_actuator_with_metadata_and_registry_id(self):
        actuator = Actuator("FILTER.ACT", object())
        meta_data = {
            'description': 'Opens a valve when temperature value exceeds 20oC'
        }
        actuator.meta_data = meta_data
        actuator.registry_id = 'UID.VALVE.023'
        self.assertEqual(actuator.meta_data, meta_data)
        self.assertEqual(actuator.meta_data['description'], 'Opens a valve when temperature value exceeds 20oC')
        self.assertEqual(actuator.registry_id, 'UID.VALVE.023')

    def test_actuator_with_input_voltage_range(self):
        actuator = Actuator("FILTER.ACT", object())
        input_voltage_range = MeasureFactory.create_measure(RecordingType.CONTINUOUS.value,
                                                            Measure(MeasurementUnit.VOLT, 0.5, 0.8))
        actuator.input_voltage_range = input_voltage_range
        self.assertEqual(actuator.input_voltage_range, input_voltage_range)
        self.assertEqual(actuator.output_voltage_range, None)

    def test_add_data_to_actuator(self):
        actuator = Actuator("FILTER.ACT", object())
        trigger_his = TriggerHistory(TriggerType.CLOSE)
        actuator.add_data([trigger_his])
        self.assertEqual(actuator.data, [trigger_his])
        self.assertEqual(actuator.data[0].trigger_type, trigger_his.trigger_type.CLOSE)
        self.assertIsNotNone(actuator.data[0].timestamp)

    def test_remove_data_from_actuator(self):
        actuator = Actuator("FILTER.ACT", object())
        trigger_his = TriggerHistory(TriggerType.OPEN_CLOSE, 1)
        actuator.add_data([trigger_his])
        self.assertEqual(actuator.data, [trigger_his])

        actuator.remove_data(trigger_his)
        self.assertEqual(actuator.data, [])
        self.assertEqual(len(actuator.data), 0)
