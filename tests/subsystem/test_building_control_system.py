from enumerations import SensorMeasure
from subsystem.building_control_system import BuildingControlSystem
from subsystem.interfaces.abstract_subsystem import AbstractSubsystem
from subsystem.hvac_system import HVACSystem
from subsystem.hvac_components.duct import Duct
from enumerations import DuctType
from enumerations import DuctSubType
from subsystem.hvac_components.fan import Fan
from enumerations import PowerState
from subsystem.hvac_components.heat_exchanger import HeatExchanger
from enumerations import HeatExchangerType
from enumerations import HeatExchangerFlowType
from subsystem.hvac_components.damper import Damper
from enumerations import DamperType
from subsystem.hvac_components.duct_connection import DuctConnection
from tests.subsystem.base_test import BaseTest
from enumerations import DuctConnectionEntityType
from subsystem.hvac_components.boiler import Boiler
from enumerations import BoilerCategory
from subsystem.hvac_components.chiller import Chiller
from enumerations import ChillerType
from measure_instruments.meter import Meter
from enumerations import MeterType
from enumerations import MeterMeasureMode
from enumerations import MeasurementUnit
from subsystem.hvac_components.cooling_tower import CoolingTower
from subsystem.hvac_components.air_volume_box import AirVolumeBox
from enumerations import AirVolumeType
from subsystem.hvac_components.variable_frequency_drive import VariableFrequencyDrive


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

    def test_building_control_system_with_hvac_system_without_ventilation(self):
        building_control_system = BuildingControlSystem("EV Control System")
        hvac_system = HVACSystem()
        building_control_system.hvac_system = hvac_system
        self.assertEqual(building_control_system.hvac_system, hvac_system)
        self.assertIsNotNone(building_control_system.hvac_system.UID)
        self.assertEqual(building_control_system.hvac_system.ventilation_system, [])

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

    def test_principal_duct_with_components_but_no_connection(self):
        duct = Duct("PR.VNT", DuctType.AIR)
        duct.duct_sub_type = DuctSubType.FRESH_AIR
        duct.add_transducer(self.presence_sensor)
        duct.add_transducer(self.temp_sensor)
        vfd = VariableFrequencyDrive('PR.VNT.VRD.01')
        fan = Fan("PR.VNT.FN.01", PowerState.ON, vfd)
        heat_exchanger = HeatExchanger("PR.VNT.HE.01", HeatExchangerType.FIN_TUBE, HeatExchangerFlowType.PARALLEL)
        damper = Damper("PR.VNT.DP.01", DamperType.BACK_DRAFT, 35)
        duct.add_heat_exchanger(heat_exchanger)
        duct.add_fan(fan)
        duct.add_damper(damper)

        self.assertEqual(duct.connections, None)
        self.assertEqual(duct.get_transducers({'measure': SensorMeasure.OCCUPANCY.value}), [self.presence_sensor])
        self.assertEqual(duct.get_fans({'name': 'PR.VNT.FN.01'})[0], fan)
        self.assertEqual(duct.get_fans({'name': 'PR.VNT.FN.01'})[0].vfd, vfd)
        self.assertEqual(duct.get_dampers(), [damper])
        self.assertEqual(duct.get_dampers()[0].percentage_opened, 35)
        self.assertEqual(duct.get_heat_exchangers(), [heat_exchanger])

    def test_principal_duct_with_supply_air_having_vav_box(self):
        duct, supply_air_duct, return_air_duct = self._init_ducts()
        vav_box = supply_air_duct.get_connected_air_volume_box()[0]
        self.assertEqual(vav_box.air_volume_type, AirVolumeType.VARIABLE_AIR_VOLUME)
        self.assertEqual(vav_box.has_heater, False)
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
