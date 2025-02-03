from metamenth.enumerations import MeasurementUnit
from metamenth.measure_instruments.meter import Meter
from metamenth.structure.open_space import OpenSpace
from metamenth.enumerations import OpenSpaceType
from metamenth.enumerations import RoomType
from metamenth.enumerations import MeterType
from metamenth.transducers.sensor import Sensor
from metamenth.enumerations import SensorMeasure
from metamenth.enumerations import SensorMeasureType
from tests.structure.base_test import BaseTest
from metamenth.enumerations import MeterMeasureMode
from metamenth.measure_instruments.meter_measure import MeterMeasure
from metamenth.subsystem.appliance import Appliance
from metamenth.enumerations import SensorLogType
from metamenth.enumerations import ApplianceType
from metamenth.enumerations import ApplianceCategory
from metamenth.subsystem.hvac_components.damper import Damper
from metamenth.enumerations import DamperType
from metamenth.transducers.actuator import Actuator
from metamenth.energysystem.electricals.uninterruptible_power_supply import UninterruptiblePowerSupply
from metamenth.enumerations import UPSPhase
from metamenth.enumerations import PowerState
from metamenth.energysystem.storage_system.battery import Battery
from metamenth.enumerations import BatteryTech
from metamenth.enumerations import EnergySource
from metamenth.energysystem.electricals.alternator import Alternator
from metamenth.energysystem.electricals.automatic_transfer_switch import AutomaticTransferSwitch
from metamenth.misc import MeasureFactory
from metamenth.enumerations import RecordingType
from metamenth.datatypes.measure import Measure
from datetime import datetime
from datetime import timedelta
from metamenth.datatypes.operational_schedule import OperationalSchedule


class TestRoom(BaseTest):

    def test_classroom_with_name_and_area(self):
        self.assertEqual(self.room.room_type, RoomType.BEDROOM)
        self.assertEqual(self.room.area.value, 45)
        self.assertEqual(self.room.area.measurement_unit, MeasurementUnit.SQUARE_METERS)
        self.assertEqual(self.room.name, "Room 145")
        self.assertEqual(self.room.location, "")
        self.assertIsNone(self.room.meter)

    def test_classroom_with_power_meter_with_different_location(self):
        try:
            power_meter = Meter(meter_location="huz.cab.err", manufacturer="Honeywell",
                                measurement_frequency=5, measurement_unit=MeasurementUnit.KILOWATTS,
                                meter_type=MeterType.ELECTRICITY, measure_mode=MeterMeasureMode.MANUAL)
            self.room.meter = power_meter
        except ValueError as err:
            self.assertEqual(err.__str__(), "what3words location of meter should be the same as space")

    def test_classroom_with_power_meter_and_same_location(self):
        self.room.location = "huz.cab.err"
        power_meter = Meter("huz.cab.err", manufacturer="Honeywell", measurement_frequency=5,
                            measurement_unit=MeasurementUnit.KILOWATTS, meter_type=MeterType.ELECTRICITY,
                            measure_mode=MeterMeasureMode.AUTOMATIC)
        power_meter.add_meter_measure(MeterMeasure(2))
        power_meter.add_meter_measure(MeterMeasure(5))
        self.room.meter = power_meter
        self.assertEqual(self.room.meter.meter_type, power_meter.meter_type)
        self.assertEqual(len(self.room.meter.get_meter_measures()), 2)
        self.assertEqual(self.room.location, power_meter.meter_location)

    def test_classroom_with_adjacent_hall(self):
        hall = OpenSpace("LECTURE_HALL_2", self.area, OpenSpaceType.HALL)
        self.room.add_adjacent_space(hall)
        self.assertEqual(len(self.room.get_adjacent_spaces()), 1)
        self.assertEqual(self.room.get_adjacent_space_by_name(hall.name), hall)
        self.assertEqual(self.room.get_adjacent_space_by_uid(hall.UID).space_type, OpenSpaceType.HALL)

    def test_classroom_as_adjacent_room_to_hall(self):
        self.hall = OpenSpace("LECTURE_HALL_3", self.area, OpenSpaceType.HALL)
        self.room.add_adjacent_space(self.hall)
        self.hall.add_adjacent_space(self.room)
        self.assertEqual(self.hall.get_adjacent_space_by_uid(self.room.UID), self.room)
        self.assertEqual(self.hall.get_adjacent_space_by_uid(self.room.UID).room_type, RoomType.BEDROOM)

    def test_remove_adjacent_space(self):
        self.hall = OpenSpace("LECTURE_HALL_4", self.area, OpenSpaceType.HALL)
        self.room.add_adjacent_space(self.hall)
        self.assertEqual(self.room.get_adjacent_space_by_uid(self.hall.UID), self.hall)

        self.room.remove_adjacent_space(self.hall)
        self.assertEqual(self.room.get_adjacent_spaces(), [])

    def test_add_existing_adjacent_space(self):
        self.hall = OpenSpace("LECTURE_HALL_5", self.area, OpenSpaceType.HALL)
        self.room.add_adjacent_space(self.hall)
        self.room.add_adjacent_space(self.hall)
        # should not add an adjacent space that already exists
        self.assertEqual(len(self.room.get_adjacent_spaces()), 1)
        self.assertEqual(self.room.get_adjacent_spaces(), [self.hall])

    def test_classroom_with_co2_and_temp_sensors(self):
        co2_sensor = Sensor("Co2_Sensor", SensorMeasure.CARBON_DIOXIDE,
                            MeasurementUnit.PARTS_PER_MILLION, SensorMeasureType.PT_100, 5)
        temp_sensor = Sensor("Temp_Sensor", SensorMeasure.TEMPERATURE,
                             MeasurementUnit.DEGREE_CELSIUS, SensorMeasureType.PT_100, 5)
        self.room.add_transducer(co2_sensor)
        self.room.add_transducer(temp_sensor)
        self.assertEqual(len(self.room.get_transducers()), 2)
        self.assertEqual(self.room.get_transducer_by_name(co2_sensor.name).measure, SensorMeasure.CARBON_DIOXIDE)
        self.assertEqual(self.room.get_transducer_by_name(temp_sensor.name).measure, SensorMeasure.TEMPERATURE)
        self.assertEqual(self.room.get_transducer_by_name(co2_sensor.name).data_frequency, co2_sensor.data_frequency)

    def test_classroom_with_pressure_sensors(self):
        pr_sensor = Sensor("PR Sensor", SensorMeasure.PRESSURE,
                           MeasurementUnit.PASCAL, SensorMeasureType.PT_100, 5)
        try:
            self.room.add_transducer(pr_sensor)
        except ValueError as err:
            self.assertIn("Space sensors must be one of the following", err.__str__())

    def test_classroom_with_actuator(self):
        damper = Damper("PR.VNT.DP.01", DamperType.BACK_DRAFT)
        actuator = Actuator("DAMPER.ACT", damper)

        try:
            self.room.add_transducer(actuator)
        except ValueError as err:
            self.assertEqual("Actuators cannot be added to spaces directly", err.__str__())

    def test_add_existing_sensor_with_the_same_name(self):
        co2_sensor = Sensor("Co2_Sensor", SensorMeasure.CARBON_DIOXIDE,
                            MeasurementUnit.PARTS_PER_MILLION, SensorMeasureType.PT_100, 5)
        temp_sensor = Sensor("Co2_Sensor", SensorMeasure.TEMPERATURE,
                             MeasurementUnit.DEGREE_CELSIUS, SensorMeasureType.PT_100, 8)
        self.room.add_transducer(co2_sensor)
        self.room.add_transducer(temp_sensor)

        self.assertEqual(len(self.room.get_transducers()), 1)
        self.assertEqual(self.room.get_transducer_by_name(co2_sensor.name).data_frequency, 5)

    def test_remove_transducer_from_room(self):
        co2_sensor = Sensor("Co2_Sensor", SensorMeasure.CARBON_DIOXIDE,
                            MeasurementUnit.PARTS_PER_MILLION, SensorMeasureType.PT_100, 5)
        temp_sensor = Sensor("Temp_Sensor", SensorMeasure.TEMPERATURE,
                             MeasurementUnit.DEGREE_CELSIUS, SensorMeasureType.PT_100, 5)
        self.room.add_transducer(co2_sensor)
        self.room.add_transducer(temp_sensor)
        self.assertEqual(len(self.room.get_transducers()), 2)

        self.room.remove_transducer(co2_sensor)

        self.assertEqual(len(self.room.get_transducers()), 1)
        self.assertEqual(self.room.get_transducer_by_uid(temp_sensor.UID), temp_sensor)

        self.room.remove_transducer(temp_sensor)
        self.assertEqual(len(self.room.get_transducers()), 0)

    def test_room_with_thermostat(self):
        co2_sensor = Sensor("Co2_Sensor", SensorMeasure.CARBON_DIOXIDE,
                            MeasurementUnit.PARTS_PER_MILLION, SensorMeasureType.PT_100, 5)

        temp_sensor = Sensor("TEMPERATURE.SENSOR", SensorMeasure.TEMPERATURE, MeasurementUnit.DEGREE_CELSIUS,
                             SensorMeasureType.THERMO_COUPLE_TYPE_A, 900, sensor_log_type=SensorLogType.POLLING)

        thermostat = Appliance("Thermostat", [ApplianceCategory.OFFICE, ApplianceCategory.SMART],
                               ApplianceType.THERMOSTAT)

        thermostat.add_transducer(temp_sensor)
        thermostat.add_transducer(co2_sensor)

        self.room.add_appliance(thermostat)
        self.assertEqual(self.room.get_appliance_by_name("Thermostat"), thermostat)
        self.assertEqual(self.room.get_appliance_by_uid(thermostat.UID).get_transducers(), [temp_sensor, co2_sensor])

    def test_room_with_duplicate_thermostats(self):
        co2_sensor = Sensor("Co2_Sensor", SensorMeasure.CARBON_DIOXIDE,
                            MeasurementUnit.PARTS_PER_MILLION, SensorMeasureType.PT_100, 5)

        temp_sensor = Sensor("TEMPERATURE.SENSOR", SensorMeasure.TEMPERATURE, MeasurementUnit.DEGREE_CELSIUS,
                             SensorMeasureType.THERMO_COUPLE_TYPE_A, 900, sensor_log_type=SensorLogType.POLLING)

        thermostat = Appliance("Thermostat", [ApplianceCategory.OFFICE, ApplianceCategory.SMART],
                               ApplianceType.THERMOSTAT)

        thermostat.add_transducer(temp_sensor)
        thermostat.add_transducer(co2_sensor)

        self.room.add_appliance(thermostat)
        self.room.add_appliance(thermostat)

        self.assertEqual(len(self.room.get_appliances()), 1)
        self.assertEqual(self.room.get_appliances(), [thermostat])

    def test_room_with_ups(self):
        ups = UninterruptiblePowerSupply("UPS", PowerState.ON, UPSPhase.THREE)
        battery = Battery("Battery", True, MeasurementUnit.KILOWATTS_PER_HOUR, EnergySource.GRID,
                          BatteryTech.NICKEL)
        ups.add_storage_system(battery)
        ups.noise_filtering = True
        ups.surge_suppression = True
        self.room.add_energy_system(ups)

        self.assertEqual(self.room.get_energy_systems({'name': 'UPS'}), [ups])
        self.assertEqual(self.room.get_energy_systems({'name': 'UPS'})[0].get_storage_system_by_name(battery.name),
                         battery)

        ups.remove_storage_system(battery)
        self.assertIsNone(ups.get_storage_system_by_name(battery.name))

    def test_room_with_ats_and_alternator(self):
        ats = AutomaticTransferSwitch("ATS", PowerState.ON)
        power_rating = MeasureFactory.create_measure(RecordingType.BINARY.value,
                                      Measure(MeasurementUnit.WATTS, 10000))
        alternator = Alternator("Alternator")
        alternator.power_rating = power_rating
        schedule = OperationalSchedule("WEEKENDS", datetime.now(), datetime.now() + timedelta(days=2))
        alternator.schedulable_entity.add_schedule(schedule)
        self.room.add_energy_system(ats)
        self.room.add_energy_system(alternator)
        self.assertEqual(self.room.get_energy_systems(), [ats, alternator])
        self.assertEqual(self.room.get_energy_systems({'name': alternator.name}), [alternator])
        self.assertEqual(self.room.get_energy_systems({'name': alternator.name})[0].power_rating, power_rating)
        self.assertEqual(self.room.get_energy_systems({'name': alternator.name})[0].schedulable_entity.get_schedule_by_name("WEEKENDS"), schedule)

        self.room.remove_energy_system(ats)
        self.assertEqual(self.room.get_energy_systems(), [alternator])