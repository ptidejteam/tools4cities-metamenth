from metamenth.enumerations import SensorMeasure
from metamenth.subsystem.building_control_system import BuildingControlSystem
from metamenth.subsystem.interfaces.abstract_subsystem import AbstractSubsystem
from metamenth.subsystem.hvac_system import HVACSystem
from metamenth.subsystem.hvac_components.duct import Duct
from metamenth.subsystem.hvac_components.filter import Filter
from metamenth.enumerations import DuctType
from metamenth.enumerations import DuctSubType
from metamenth.subsystem.hvac_components.fan import Fan
from metamenth.measure_instruments.status_measure import StatusMeasure
from metamenth.subsystem.hvac_components.heat_exchanger import HeatExchanger
from metamenth.enumerations import HeatExchangerType
from metamenth.enumerations import HeatExchangerFlowType
from metamenth.subsystem.hvac_components.damper import Damper
from metamenth.enumerations import DamperType
from metamenth.subsystem.hvac_components.duct_connection import DuctConnection
from tests.subsystem.base_test import BaseTest
from metamenth.enumerations import DuctConnectionEntityType
from metamenth.subsystem.hvac_components.boiler import Boiler
from metamenth.enumerations import BoilerCategory
from metamenth.subsystem.hvac_components.chiller import Chiller
from metamenth.enumerations import ChillerType
from metamenth.measure_instruments.meter import Meter
from metamenth.enumerations import MeterType
from metamenth.enumerations import MeterMeasureMode
from metamenth.enumerations import MeasurementUnit
from metamenth.subsystem.hvac_components.cooling_tower import CoolingTower
from metamenth.subsystem.hvac_components.air_volume_box import AirVolumeBox
from metamenth.enumerations import AirVolumeType
from metamenth.subsystem.hvac_components.variable_frequency_drive import VariableFrequencyDrive
from metamenth.enumerations import ZoneType
from metamenth.enumerations import HVACType
from metamenth.virtual.zone import Zone
from metamenth.subsystem.ventilation_system import VentilationSystem
from metamenth.enumerations import VentilationType
from metamenth.subsystem.thermal_storage import ThermalStorage
from metamenth.subsystem.radiant_slab import RadiantSlab
from metamenth.subsystem.baseboard_heater import BaseboardHeater
from metamenth.enumerations import RadiantSlabType
from metamenth.enumerations import HeatingType
from metamenth.subsystem.interfaces.abstract_ventilation_component import AbstractVentilationComponent
from metamenth.subsystem.hvac_components.heat_pump import HeatPump
from metamenth.enumerations import HeatSource
from metamenth.subsystem.hvac_components.condenser import Condenser
from metamenth.subsystem.hvac_components.compressor import Compressor
from metamenth.enumerations import RefrigerantType
from metamenth.enumerations import CoilMaterial
from metamenth.enumerations import CompressorType
from metamenth.datatypes.operational_schedule import OperationalSchedule
from datetime import datetime
from datetime import timedelta
from metamenth.enumerations import PowerState
from metamenth.measure_instruments.damper_position import DamperPosition
from metamenth.enumerations import FilterType
from metamenth.enumerations import PumpType
from metamenth.subsystem.hvac_components.pump import Pump
from metamenth.enumerations import RoomType
from metamenth.enumerations import FCUType
from metamenth.enumerations import FCUPipeSystem
from metamenth.subsystem.hvac_components.fan_coil_unit import FanCoilUnit


class TestBuildingControlSystem(BaseTest):

    def _init_ducts(self):
        duct = Duct("PR.VNT", DuctType.AIR)

        supply_air_duct = Duct("SUPP.VNT.01", DuctType.AIR)
        supply_air_duct.duct_sub_type = DuctSubType.FRESH_AIR

        # connect supply air duct to the floor it supplies air to
        supply_duct_conn = DuctConnection()
        supply_duct_conn.add_entity(DuctConnectionEntityType.DESTINATION, self.floor)

        # connect VAV box to the supply air duct
        room_vav_box = AirVolumeBox('PR.VNT.VAV.01', AirVolumeType.VARIABLE_AIR_VOLUME)
        room_vav_box.inlet_dampers = [Damper('PR.VNT.DMP.03', DamperType.MANUAL_VOLUME)]

        supply_air_duct.add_connected_air_volume_box(room_vav_box)
        self.room.add_hvac_component(room_vav_box)

        # add the principal duct as the source to the supply air duct
        supply_duct_conn.add_entity(DuctConnectionEntityType.SOURCE, duct)
        supply_air_duct.connections = supply_duct_conn

        # connect principal ventilation duct to supply air duct
        principal_duct_conn = DuctConnection()
        principal_duct_conn.add_entity(DuctConnectionEntityType.DESTINATION, supply_air_duct)
        duct.connections = principal_duct_conn

        return_air_duct = Duct("RET.VNT.01", DuctType.AIR)
        return_air_duct.duct_sub_type = DuctSubType.RETURN_AIR

        # add the floor as the source to the return air duct (it takes 'used' air from the floor to the building
        return_air_conn = DuctConnection()
        return_air_conn.add_entity(DuctConnectionEntityType.SOURCE, self.floor)
        return_air_conn.add_entity(DuctConnectionEntityType.SOURCE, self.room)
        return_air_duct.connections = return_air_conn

        # add the return air duct as a source to the principal ventilation duct to recuperate heat from waste aire
        principal_duct_conn.add_entity(DuctConnectionEntityType.SOURCE, return_air_duct)

        fan = Fan("PR.VNT.FN.01", PowerState.ON, None)
        duct.add_fan(fan)
        return duct, supply_air_duct, return_air_duct

    def _connect_components(self, principal_duct):
        heat_exchanger = HeatExchanger("PR.VNT.HE.01", HeatExchangerType.FIN_TUBE, HeatExchangerFlowType.PARALLEL)
        principal_duct.add_heat_exchanger(heat_exchanger)

        boiler = Boiler('PR.VNT.BL.01', BoilerCategory.NATURAL_GAS, PowerState.ON)
        chiller = Chiller('PR.VNT.CL.01', ChillerType.WATER_COOLED, PowerState.ON)

        # create a duct that connects the chiller to heat exchanger
        chiller_heat_exchanger_tube = Duct('TB.CL.HE.01', DuctType.WATER_WITH_ANTI_FREEZE)
        chiller_heat_exchanger_tube.duct_sub_type = DuctSubType.COLD_WATER

        ch_ht_tube_connections = DuctConnection()
        ch_ht_tube_connections.is_loop = True
        ch_ht_tube_connections.add_entity(DuctConnectionEntityType.SOURCE, chiller)
        ch_ht_tube_connections.add_entity(DuctConnectionEntityType.DESTINATION, heat_exchanger)
        chiller_heat_exchanger_tube.connections = ch_ht_tube_connections

        # create a duct that connects the boiler to heat exchanger
        boiler_heat_exchanger_tube = Duct('TB.BL.HE.01', DuctType.WATER)
        boiler_heat_exchanger_tube.duct_sub_type = DuctSubType.HOT_WATER
        bl_ht_tube_connections = DuctConnection()
        bl_ht_tube_connections.is_loop = True
        bl_ht_tube_connections.add_entity(DuctConnectionEntityType.SOURCE, boiler)
        bl_ht_tube_connections.add_entity(DuctConnectionEntityType.DESTINATION, heat_exchanger)
        boiler_heat_exchanger_tube.connections = bl_ht_tube_connections

        # indicate the tubes the heat exchanger, chiller and boiler are connected to
        heat_exchanger.add_duct(chiller_heat_exchanger_tube)
        heat_exchanger.add_duct(boiler_heat_exchanger_tube)

        boiler.add_duct(boiler_heat_exchanger_tube)
        chiller.add_duct(chiller_heat_exchanger_tube)

        return principal_duct, chiller, boiler, heat_exchanger, chiller_heat_exchanger_tube, boiler_heat_exchanger_tube

    def test_building_control_system_with_none_hvac_system(self):
        building_control_system = BuildingControlSystem("EV Control System")
        self.assertIsInstance(building_control_system, AbstractSubsystem)
        self.assertEqual(building_control_system.hvac_system, None)

    def test_heat_pump_serving_specific_spaces(self):
        condenser = Condenser("PR.VNT.CD.01", RefrigerantType.R404A, CoilMaterial.COPPER)
        compressor = Compressor("PR.VNT.CP.01", CompressorType.RECIPROCATING_SEMI_HERMETIC)
        heat_exchanger = HeatExchanger("PR.VNT.HE.01", HeatExchangerType.FIN_TUBE, HeatExchangerFlowType.PARALLEL)
        heat_pump = HeatPump("PR.VNT.HP.01", HeatSource.AQUIFER, condenser, compressor)
        heat_pump.add_heat_exchanger(heat_exchanger)
        heat_pump.add_spaces([self.room, self.floor, self.hall])

        schedule = OperationalSchedule("WEEKDAYS", datetime.now(), datetime.now() + timedelta(days=5))
        heat_pump.schedulable_entity.add_schedule(schedule)

        self.assertEqual(heat_pump.schedulable_entity.get_schedules(), [schedule])
        self.assertEqual(heat_pump.heat_exchangers, [heat_exchanger])
        self.assertEqual(heat_pump.get_spaces({'name': self.hall.name}), [self.hall])
        self.assertEqual(heat_pump.condenser, condenser)

    def test_add_fan_to_room(self):
        try:
            vfd = VariableFrequencyDrive('PR.VNT.VRD.01')
            fan = Fan("PR.VNT.FN.01", PowerState.ON, vfd)
            self.room.add_hvac_component(fan)
        except ValueError as err:
            self.assertEqual(err.__str__(), "PR.VNT.FN.01 cannot be added to a space entity")

    def test_add_fan_to_open_space(self):
        try:
            vfd = VariableFrequencyDrive('PR.VNT.VRD.01')
            fan = Fan("PR.VNT.FN.01", PowerState.ON, vfd)
            self.hall.add_hvac_component(fan)
        except ValueError as err:
            self.assertEqual(err.__str__(), "PR.VNT.FN.01 cannot be added to a space entity")

    def test_add_vav_box_to_non_mechanical_room(self):
        vav_box = AirVolumeBox('PR.VNT.VAV.01', AirVolumeType.VARIABLE_AIR_VOLUME)
        self.room.add_hvac_component(vav_box)
        self.assertEqual(self.room.get_hvac_components(), [vav_box])

    def test_add_heat_exchanger_to_open_space(self):
        try:
            heat_exchanger = HeatExchanger("PR.VNT.HE.01", HeatExchangerType.FIN_TUBE, HeatExchangerFlowType.PARALLEL)
            self.hall.add_hvac_component(heat_exchanger)
        except ValueError as err:
            self.assertEqual(err.__str__(), "You can only add air volume box/ducts to open spaces")

    def test_add_heat_exchanger_to_non_mechanical_room(self):
        try:
            heat_exchanger = HeatExchanger("PR.VNT.HE.01", HeatExchangerType.FIN_TUBE, HeatExchangerFlowType.PARALLEL)
            self.room.add_hvac_component(heat_exchanger)
        except ValueError as err:
            self.assertEqual(err.__str__(), "You can only add HVAC components to mechanical rooms")

    def test_non_ducted_fcu_to_mechanical_room(self):
        vfd = VariableFrequencyDrive('PR.VNT.VRD.01')
        fan = Fan("PR.VNT.FN.01", PowerState.ON, vfd)
        heat_exchanger = HeatExchanger("PR.VNT.HE.01", HeatExchangerType.FIN_TUBE, HeatExchangerFlowType.PARALLEL)
        fcu = FanCoilUnit('FCU.01', heat_exchanger, fan, FCUType.STANDALONE, FCUPipeSystem.FOUR_PIPE, False)
        self.room.room_type = RoomType.MECHANICAL
        self.room.add_hvac_component(fcu)
        self.assertEqual(self.room.get_hvac_components({'name': 'FCU.01'}), [fcu])

    def test_ducted_fcu_to_mechanical_room(self):
        vfd = VariableFrequencyDrive('PR.VNT.VRD.01')
        fan = Fan("PR.VNT.FN.01", PowerState.ON, vfd)
        heat_exchanger = HeatExchanger("PR.VNT.HE.01", HeatExchangerType.FIN_TUBE, HeatExchangerFlowType.PARALLEL)
        fcu = FanCoilUnit('FCU.01', heat_exchanger, fan, FCUType.STANDALONE, FCUPipeSystem.FOUR_PIPE)
        self.room.room_type = RoomType.MECHANICAL
        self.room.add_hvac_component(fcu)
        self.assertEqual(self.room.get_hvac_components({'name': 'FCU.01'}), [fcu])

    def test_ducted_fcu_to_non_mechanical_room(self):
        try:
            vfd = VariableFrequencyDrive('PR.VNT.VRD.01')
            fan = Fan("PR.VNT.FN.01", PowerState.ON, vfd)
            heat_exchanger = HeatExchanger("PR.VNT.HE.01", HeatExchangerType.FIN_TUBE, HeatExchangerFlowType.PARALLEL)
            fcu = FanCoilUnit('FCU.01', heat_exchanger, fan, FCUType.STANDALONE, FCUPipeSystem.FOUR_PIPE)
            self.room.add_hvac_component(fcu)
        except ValueError as err:
            self.assertEqual(err.__str__(), 'You can only add HVAC components to mechanical rooms')

    def test_add_non_ducted_fcu_to_duct(self):
        try:
            vfd = VariableFrequencyDrive('PR.VNT.VRD.01')
            fan = Fan("PR.VNT.FN.01", PowerState.ON, vfd)
            heat_exchanger = HeatExchanger("PR.VNT.HE.01", HeatExchangerType.FIN_TUBE, HeatExchangerFlowType.PARALLEL)
            fcu = FanCoilUnit('FCU.01', heat_exchanger, fan, FCUType.STANDALONE, FCUPipeSystem.FOUR_PIPE, False)

            duct = Duct("VNT", DuctType.AIR)
            conn = DuctConnection()
            conn.add_entity(DuctConnectionEntityType.SOURCE, fcu)
            duct.connections = conn
        except ValueError as err:
            self.assertEqual(err.__str__(), "FCU.01 cannot be connected to a duct")

    def test_add_ducted_fcu_to_duct(self):
        vfd = VariableFrequencyDrive('PR.VNT.VRD.01')
        fan = Fan("PR.VNT.FN.01", PowerState.ON, vfd)
        heat_exchanger = HeatExchanger("PR.VNT.HE.01", HeatExchangerType.FIN_TUBE, HeatExchangerFlowType.PARALLEL)
        fcu = FanCoilUnit('FCU.01', heat_exchanger, fan, FCUType.STANDALONE, FCUPipeSystem.FOUR_PIPE)
        duct = Duct("VNT", DuctType.AIR)
        conn = DuctConnection()
        conn.add_entity(DuctConnectionEntityType.SOURCE, fcu)
        duct.connections = conn
        self.assertEqual(duct.connections.get_source_entities(), [fcu])

    def test_add_boiler_to_mechanical_room(self):
        boiler = Boiler('PR.VNT.BL.01', BoilerCategory.NATURAL_GAS, PowerState.ON)
        self.room.room_type = RoomType.MECHANICAL
        self.room.add_hvac_component(boiler)
        self.assertEqual(self.room.get_hvac_components(), [boiler])

    def test_building_control_system_with_hvac_system_without_ventilation(self):
        building_control_system = BuildingControlSystem("EV Control System")
        hvac_system = HVACSystem()
        building_control_system.hvac_system = hvac_system
        self.assertEqual(building_control_system.hvac_system, hvac_system)
        self.assertIsNotNone(building_control_system.hvac_system.UID)
        self.assertEqual(building_control_system.hvac_system.ventilation_systems, [])

    def test_principal_duct_with_no_components(self):
        duct = Duct("PR.VNT", DuctType.AIR)
        duct.duct_sub_type = DuctSubType.FRESH_AIR
        duct.add_transducer(self.presence_sensor)
        duct.add_transducer(self.temp_sensor)
        self.assertEqual(duct.connections, None)
        self.assertEqual(duct.get_heat_exchangers(), [])
        self.assertEqual(duct.get_dampers(), [])
        self.assertEqual(duct.get_fans(), [])
        self.assertEqual(duct.get_transducer_by_name("PRESENCE.SENSOR"), self.presence_sensor)
        self.assertEqual(duct.get_transducer_by_name("TEMP.SENSOR"), self.temp_sensor)
        self.assertEqual(duct.get_transducers(), [self.presence_sensor, self.temp_sensor])

    def test_add_filters_to_duct(self):
        duct = Duct("PR.VNT", DuctType.AIR)
        duct.duct_sub_type = DuctSubType.FRESH_AIR
        filter_one = Filter("FLT.VNT", FilterType.ELECTROSTATIC)
        filter_two = Filter("FLT.VNT.02", FilterType.FIBREGLASS)
        duct.add_filter(filter_one)
        duct.add_filter(filter_two)

        self.assertEqual(duct.connections, None)
        self.assertEqual(duct.get_heat_exchangers(), [])
        self.assertEqual(duct.get_dampers(), [])
        self.assertEqual(duct.get_fans(), [])

        self.assertEqual(duct.get_filters(), [filter_one, filter_two])

    def test_remove_filters_from_duct(self):
        duct = Duct("PR.VNT", DuctType.AIR)
        duct.duct_sub_type = DuctSubType.FRESH_AIR
        filter_one = Filter("FLT.VNT", FilterType.ELECTROSTATIC)
        filter_two = Filter("FLT.VNT.02", FilterType.FIBREGLASS)
        duct.add_filter(filter_one)
        duct.add_filter(filter_two)

        duct.remove_filter(filter_one)

        self.assertEqual(duct.connections, None)
        self.assertEqual(duct.get_heat_exchangers(), [])
        self.assertEqual(duct.get_dampers(), [])
        self.assertEqual(duct.get_fans(), [])

        self.assertEqual(duct.get_filters(), [filter_two])

    def test_pump_chiller_connection(self):
        duct = Duct("PR.VNT", DuctType.WATER_WITH_ANTI_FREEZE)
        duct.duct_sub_type = DuctSubType.GLYCOL

        chiller = Chiller('PR.VNT.CL.01', ChillerType.WATER_COOLED, PowerState.ON)
        pump = Pump("PR.PMP", PumpType.CIRCULATOR)

        chiller_pump_connection = DuctConnection()
        chiller_pump_connection.add_entity(DuctConnectionEntityType.SOURCE, chiller)
        chiller_pump_connection.add_entity(DuctConnectionEntityType.DESTINATION, pump)
        chiller_pump_connection.is_loop = True

        duct.connections = chiller_pump_connection

        self.assertEqual(duct.connections, chiller_pump_connection)
        self.assertEqual(duct.connections.get_source_entities(), [chiller])
        self.assertEqual(duct.connections.get_destination_entities(), [pump])

    def test_remove_position_data_from_damper(self):
        damper = Damper("PR.VNT.DP.01", DamperType.BACK_DRAFT)
        dpm_pos = DamperPosition(0.85)
        damper.add_damper_position(dpm_pos)
        damper.add_damper_position(DamperPosition(0.78))
        damper.add_damper_position(DamperPosition(0.787))
        damper.add_damper_position(DamperPosition(0.765))

        damper.remove_damper_position(dpm_pos)

        self.assertEqual(len(damper.get_damper_positions()), 3)

    def test_get_position_positions_by_date(self):
        damper = Damper("PR.VNT.DP.01", DamperType.BACK_DRAFT)
        pos_date = '2024-09-23'
        dpm_pos = DamperPosition(0.85, pos_date)
        damper.add_damper_position(dpm_pos)
        damper.add_damper_position(DamperPosition(0.78))
        damper.add_damper_position(DamperPosition(0.787))
        damper.add_damper_position(DamperPosition(0.765))

        self.assertEqual(damper.get_damper_positions_by_date(pos_date, pos_date), [dpm_pos])

    def test_principal_duct_with_components_but_no_connection(self):
        duct = Duct("PR.VNT", DuctType.AIR)
        duct.duct_sub_type = DuctSubType.FRESH_AIR
        duct.add_transducer(self.presence_sensor)
        duct.add_transducer(self.temp_sensor)
        vfd = VariableFrequencyDrive('PR.VNT.VRD.01')
        fan = Fan("PR.VNT.FN.01", PowerState.ON, vfd)
        heat_exchanger = HeatExchanger("PR.VNT.HE.01", HeatExchangerType.FIN_TUBE, HeatExchangerFlowType.PARALLEL)
        damper = Damper("PR.VNT.DP.01", DamperType.BACK_DRAFT)
        damper.add_damper_position(DamperPosition(0.85))
        damper.add_damper_position(DamperPosition(0.78))
        damper.add_damper_position(DamperPosition(0.787))
        damper.add_damper_position(DamperPosition(0.765))
        duct.add_heat_exchanger(heat_exchanger)
        duct.add_fan(fan)
        duct.add_damper(damper)

        self.assertEqual(duct.connections, None)
        self.assertEqual(duct.get_transducers({'measure': SensorMeasure.OCCUPANCY.value}), [self.presence_sensor])
        self.assertEqual(duct.get_fans({'name': 'PR.VNT.FN.01'})[0], fan)
        self.assertEqual(duct.get_fans({'name': 'PR.VNT.FN.01'})[0].vfd, vfd)
        self.assertEqual(duct.get_dampers(), [damper])
        self.assertEqual(len(duct.get_dampers()[0].get_damper_positions()), 4)
        self.assertEqual(duct.get_heat_exchangers(), [heat_exchanger])

    def test_principal_duct_with_supply_air_having_vav_box(self):
        duct, supply_air_duct, return_air_duct = self._init_ducts()
        vav_box = supply_air_duct.get_connected_air_volume_boxes()[0]
        self.assertEqual(vav_box.air_volume_type, AirVolumeType.VARIABLE_AIR_VOLUME)
        self.assertEqual(vav_box.has_heating_capability, False)
        self.assertIsInstance(vav_box.inlet_dampers[0], Damper)
        self.assertEqual(vav_box.inlet_dampers[0].damper_type, DamperType.MANUAL_VOLUME)
        self.assertEqual(self.room.get_hvac_components(), [vav_box])

    def test_principal_duct_with_supply_and_return_air_ducts(self):
        duct, supply_air_duct, return_air_duct = self._init_ducts()

        self.assertIsNotNone(duct.connections)
        self.assertEqual(duct.connections.get_destination_entities(), [supply_air_duct])
        self.assertEqual(duct.connections.get_destination_entities()[0].connections.get_destination_entities(),
                         [self.floor])
        self.assertEqual(duct.connections.get_source_entities(), [return_air_duct])
        self.assertEqual(duct.connections.get_source_entities()[0].connections.get_source_entities(),
                         [self.floor, self.room])
        self.assertEqual(supply_air_duct.connections.get_source_entities(), [duct])

    def test_principal_duct_with_heat_exchanger_boiler_and_chiller(self):
        principal_duct, _, _ = self._init_ducts()
        principal_duct, chiller, boiler, heat_exchanger, chiller_heat_exchanger_tube, boiler_heat_exchanger_tube = \
            self._connect_components(principal_duct)

        self.assertEqual(principal_duct.get_heat_exchangers(), [heat_exchanger])
        self.assertEqual(principal_duct.get_heat_exchangers()[0].ducts, [chiller_heat_exchanger_tube,
                                                                         boiler_heat_exchanger_tube])
        self.assertEqual(principal_duct.get_heat_exchangers()[0].ducts[0].connections.get_source_entities(), [chiller])
        self.assertEqual(principal_duct.get_heat_exchangers()[0].ducts[0].connections.get_destination_entities(),
                         [heat_exchanger])
        self.assertEqual(boiler.ducts, [boiler_heat_exchanger_tube])
        self.assertEqual(boiler.ducts[0].connections.get_source_entities(), [boiler])
        self.assertEqual(boiler.ducts[0].connections.get_destination_entities(), [heat_exchanger])
        self.assertEqual(chiller_heat_exchanger_tube.connections.get_source_entities(), [chiller])

    def test_principal_duct_with_components_having_meters_and_sensors(self):
        principal_duct, _, _ = self._init_ducts()
        principal_duct, chiller, boiler, heat_exchanger, chiller_heat_exchanger_tube, boiler_heat_exchanger_tube = \
            self._connect_components(principal_duct)

        # add meter and sensors to chiller and boiler
        chiller.add_transducer(self.temp_sensor)
        chiller.add_transducer(self.pressure_sensor)
        flow_meter = Meter(meter_location="huz.cab.err", manufacturer="Honeywell", measurement_frequency=5,
                           measurement_unit=MeasurementUnit.LITERS_PER_SECOND, meter_type=MeterType.FLOW,
                           measure_mode=MeterMeasureMode.AUTOMATIC)
        chiller.meter = flow_meter

        boiler.add_transducer(self.temp_sensor)
        boiler.add_transducer(self.pressure_sensor)
        power_meter = Meter(meter_location="huz.cab.err", manufacturer="Honeywell", measurement_frequency=5,
                            measurement_unit=MeasurementUnit.KILOWATTS, meter_type=MeterType.POWER,
                            measure_mode=MeterMeasureMode.AUTOMATIC)
        boiler.meter = power_meter
        heat_exchanger_ducts = principal_duct.get_heat_exchangers()[0].ducts
        self.assertEqual(heat_exchanger_ducts[1].connections.get_source_entities()[0].meter, power_meter)
        self.assertEqual(heat_exchanger_ducts[1].connections.get_source_entities()[0].get_transducers(),
                         [self.temp_sensor, self.pressure_sensor])
        self.assertEqual(heat_exchanger_ducts[0].connections.get_source_entities()[0].meter, flow_meter)
        self.assertEqual(heat_exchanger_ducts[0].connections.get_source_entities()[0].get_transducers(),
                         [self.temp_sensor, self.pressure_sensor])

    def test_principal_duct_with_components_and_cooling_tower(self):
        principal_duct, _, _ = self._init_ducts()
        principal_duct, chiller, _, heat_exchanger, _, _ = self._connect_components(principal_duct)
        cooling_tower = CoolingTower("PR.VNT.CLT.01")
        tower_chiller_tube = Duct('TB.CL.CLT.01', DuctType.WATER)
        tower_chiller_conn = DuctConnection()
        tower_chiller_conn.add_entity(DuctConnectionEntityType.SOURCE, cooling_tower)
        tower_chiller_conn.add_entity(DuctConnectionEntityType.DESTINATION, chiller)
        tower_chiller_conn.is_loop = True
        tower_chiller_tube.connections = tower_chiller_conn
        chiller.add_duct(tower_chiller_tube)
        cooling_tower.add_duct(tower_chiller_tube)

        vnt_chiller = principal_duct.get_heat_exchangers()[0].ducts[0].connections.get_source_entities()[0]
        self.assertEqual(vnt_chiller, chiller)
        self.assertEqual(vnt_chiller.ducts[1], tower_chiller_tube)
        self.assertEqual(vnt_chiller.ducts[1].connections.is_loop, True)
        self.assertEqual(vnt_chiller.ducts[1].connections.get_source_entities(), [cooling_tower])
        self.assertEqual(vnt_chiller.ducts[0].connections.get_destination_entities(), [heat_exchanger])

    def test_ventilation_system_with_supply_duct_for_specific_zone(self):
        principal_duct, supply_air_duct, _ = self._init_ducts()

        warm_zone = Zone("WARM_ZONE", ZoneType.HVAC, HVACType.PERIMETER)
        cold_zone = Zone("COLD_ZONE", ZoneType.HVAC, HVACType.INTERIOR)

        supply_air_duct.add_zone(warm_zone, self.building)
        supply_air_duct.add_zone(cold_zone, self.building)
        supply_air_duct.connections.add_entity(DuctConnectionEntityType.DESTINATION, self.room)

        self.room.add_zone(cold_zone, self.building)
        self.hall.add_zone(warm_zone, self.building)

        supp_duct = principal_duct.connections.get_destination_entities()[0]
        room_zone = supp_duct.connections.get_destination_entities({'name': self.room.name})[0].get_zones()[0]

        self.assertEqual(supply_air_duct, supp_duct)
        self.assertEqual(supp_duct.get_zones(), [warm_zone, cold_zone])
        self.assertEqual(room_zone, cold_zone)
        self.assertEqual(self.building.get_zones(), [warm_zone, cold_zone])

    def test_ventilation_system_with_principal_duct(self):
        principal_duct, supply_air_duct, return_air_duct = self._init_ducts()
        principal_duct, chiller, boiler, heat_exchanger, _, _ = self._connect_components(principal_duct)
        ventilation_system = VentilationSystem(VentilationType.AIR_HANDLING_UNIT, principal_duct)

        vnt_chiller = ventilation_system.principal_duct \
            .get_heat_exchangers()[0].ducts[0].connections.get_source_entities()[0]
        vnt_boiler = ventilation_system.principal_duct \
            .get_heat_exchangers()[0].ducts[1].connections.get_source_entities()[0]

        self.assertEqual(ventilation_system.principal_duct.get_heat_exchangers(), [heat_exchanger])
        self.assertEqual(ventilation_system.principal_duct.connections.get_source_entities()[0], return_air_duct)
        self.assertEqual(ventilation_system.principal_duct.connections.get_destination_entities()[0], supply_air_duct)
        self.assertEqual(vnt_chiller, chiller)
        self.assertEqual(vnt_boiler, boiler)
        self.assertEqual(ventilation_system.get_components(), [])

    def test_ventilation_system_with_components(self):
        principal_duct, supply_air_duct, return_air_duct = self._init_ducts()
        ventilation_system = VentilationSystem(VentilationType.AIR_HANDLING_UNIT, principal_duct)

        supply_air_duct.connections.add_entity(DuctConnectionEntityType.DESTINATION, self.room)
        supply_air_duct.connections.add_entity(DuctConnectionEntityType.DESTINATION, self.hall)

        radiant_slab = RadiantSlab('PR.VNT.RS.01', RadiantSlabType.AIR_HEATED)
        baseboard_heater = BaseboardHeater('PR.VNT.BH.01', HeatingType.ELECTRIC, PowerState.ON)
        thermal_storage = ThermalStorage('PR.VNT.TS.01')

        self.room.add_hvac_component(radiant_slab)
        self.hall.add_hvac_component(baseboard_heater)

        ventilation_system.add_component(radiant_slab)
        ventilation_system.add_component(thermal_storage)
        ventilation_system.add_component(baseboard_heater)

        supp_duct_room_radiant_slab = supply_air_duct.connections.get_destination_entities(
            {'name': self.room.name})[0].get_hvac_components({'name': radiant_slab.name})[0]

        self.assertEqual(ventilation_system.get_components({'name': radiant_slab.name})[0], radiant_slab)
        self.assertEqual(ventilation_system.get_components({'name': baseboard_heater.name})[0], baseboard_heater)
        self.assertEqual(ventilation_system.get_components({'name': thermal_storage.name})[0], thermal_storage)
        self.assertEqual(self.hall.get_hvac_components(), [baseboard_heater])
        self.assertIsInstance(self.room.get_hvac_components()[0], AirVolumeBox)
        self.assertEqual(self.room.get_hvac_components({'name': radiant_slab.name})[0], radiant_slab)
        self.assertEqual(supp_duct_room_radiant_slab, radiant_slab)

    def test_hvac_components_with_status_data(self):
        principal_duct, supply_air_duct, return_air_duct = self._init_ducts()
        principal_duct, chiller, boiler, heat_exchanger, _, _ = self._connect_components(principal_duct)
        chiller.add_status_measure(StatusMeasure(PowerState.ON.value))
        chiller.add_status_measure(StatusMeasure(PowerState.OFF.value))
        boiler.add_status_measure(StatusMeasure(PowerState.OFF.value))
        boiler.add_status_measure(StatusMeasure(PowerState.OFF.value))
        heat_exchanger.add_status_measure(StatusMeasure(PowerState.OFF.value))
        self.assertEqual(chiller.get_status_measure({'value': PowerState.ON.value})[0].value, PowerState.ON.value)
        self.assertEqual(len(heat_exchanger.get_status_measure()), 1)
        self.assertEqual(boiler.get_status_measure({'value': PowerState.ON.value}), [])
        self.assertEqual(len(boiler.get_status_measure({'value': PowerState.OFF.value})), 2)

    def test_hvac_system_with_a_single_ventilation_system(self):
        principal_duct, supply_air_duct, return_air_duct = self._init_ducts()
        ventilation_system = VentilationSystem(VentilationType.AIR_HANDLING_UNIT, principal_duct)

        radiant_slab = RadiantSlab('PR.VNT.RS.01', RadiantSlabType.AIR_HEATED)
        baseboard_heater = BaseboardHeater('PR.VNT.BH.01', HeatingType.ELECTRIC, PowerState.ON)
        thermal_storage = ThermalStorage('PR.VNT.TS.01')

        ventilation_system.add_component(radiant_slab)
        ventilation_system.add_component(thermal_storage)
        ventilation_system.add_component(baseboard_heater)

        hvac_system = HVACSystem()
        hvac_system.add_ventilation_system(ventilation_system)

        self.assertEqual(hvac_system.ventilation_systems, [ventilation_system])
        self.assertEqual(hvac_system.ventilation_systems[0].get_components(),
                         [radiant_slab, thermal_storage, baseboard_heater])
        self.assertIsInstance(hvac_system.ventilation_systems[0].get_components({'name': thermal_storage.name})[0],
                              AbstractVentilationComponent)

    def test_building_with_hvac_control_system(self):
        building_control_system = BuildingControlSystem("EV Control System")

        principal_duct, supply_air_duct, return_air_duct = self._init_ducts()
        principal_duct, chiller, boiler, heat_exchanger, chiller_heat_exchanger_tube, boiler_heat_exchanger_tube = \
            self._connect_components(principal_duct)
        ventilation_system = VentilationSystem(VentilationType.AIR_HANDLING_UNIT, principal_duct)

        hvac_system = HVACSystem()
        hvac_system.add_ventilation_system(ventilation_system)

        building_control_system.hvac_system = hvac_system
        self.building.add_control_system(building_control_system)
        vent_sys = self.building.control_systems[0].hvac_system.ventilation_systems[0]

        self.assertEqual(self.building.control_systems, [building_control_system])
        self.assertEqual(self.building.control_systems[0].hvac_system, hvac_system)
        self.assertEqual(vent_sys.ventilation_type, VentilationType.AIR_HANDLING_UNIT)
        self.assertEqual(vent_sys.principal_duct, ventilation_system.principal_duct)
        self.assertEqual(vent_sys.principal_duct, principal_duct)
        self.assertEqual(vent_sys.principal_duct.connections.get_source_entities(), [return_air_duct])
        self.assertEqual(vent_sys.principal_duct.connections.get_destination_entities(), [supply_air_duct])
        self.assertEqual(vent_sys.principal_duct.connections.get_destination_entities()[0]
                         .connections.get_destination_entities(), [self.floor])
