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


class TestBuildingControlSystem(BaseTest):

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

    def test_principal_ventilation_duct_with_no_components(self):
        duct = Duct("Varannes Principal Duct", DuctType.AIR)
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

    def test_principal_ventilation_duct_with_components_but_no_connection(self):
        duct = Duct("Varannes Principal Duct", DuctType.AIR)
        duct.duct_sub_type = DuctSubType.FRESH_AIR
        duct.add_transducer(self.presence_sensor)
        duct.add_transducer(self.temp_sensor)

        fan = Fan("PR.VNT.FN.01", PowerState.ON, True)
        heat_exchanger = HeatExchanger("PR.VNT.HE.01", HeatExchangerType.FIN_TUBE, HeatExchangerFlowType.PARALLEL)
        damper = Damper("PR.VNT.DP.01", DamperType.BACK_DRAFT, 35)
        duct.add_heat_exchanger(heat_exchanger)
        duct.add_fan(fan)
        duct.add_damper(damper)

        self.assertEqual(duct.connections, None)
        self.assertEqual(duct.get_transducers({'measure': SensorMeasure.OCCUPANCY.value}), [self.presence_sensor])
        self.assertEqual(duct.get_fans({'name': 'PR.VNT.FN.01'})[0], fan)
        self.assertEqual(duct.get_dampers(), [damper])
        self.assertEqual(duct.get_dampers()[0].percentage_opened, 35)
        self.assertEqual(duct.get_heat_exchangers(), [heat_exchanger])

    def test_principal_ventilation_duct_with_supply_and_return_air_ducts(self):
        duct = Duct("Varannes Principal Duct", DuctType.AIR)

        supply_air_duct = Duct("SUPP.AIR.01", DuctType.AIR)
        supply_air_duct.duct_sub_type = DuctSubType.FRESH_AIR

        # connect supply air duct to the floor it supplies air to
        supply_duct_conn = DuctConnection()
        supply_duct_conn.add_entity(DuctConnectionEntityType.DESTINATION, self.floor)

        # add the principal duct as the source to the supply air duct
        supply_duct_conn.add_entity(DuctConnectionEntityType.SOURCE, duct)
        supply_air_duct.connections = supply_duct_conn

        # connect principal ventilation duct to supply air duct
        principal_duct_conn = DuctConnection()
        principal_duct_conn.add_entity(DuctConnectionEntityType.DESTINATION, supply_air_duct)
        duct.connections = principal_duct_conn

        return_air_duct = Duct("RET.AIR.01", DuctType.AIR)
        return_air_duct.duct_sub_type = DuctSubType.RETURN_AIR

        # add the floor as the source to the return air duct (it takes 'used' air from the floor to the building
        return_air_conn = DuctConnection()
        return_air_conn.add_entity(DuctConnectionEntityType.SOURCE, self.floor)
        return_air_conn.add_entity(DuctConnectionEntityType.SOURCE, self.room)
        return_air_duct.connections = return_air_conn

        # add the return air duct as a source to the principal ventilation duct to recuperate heat from waste aire
        principal_duct_conn.add_entity(DuctConnectionEntityType.SOURCE, return_air_duct)

        fan = Fan("PR.VNT.FN.01", PowerState.ON, True)
        duct.add_fan(fan)

        self.assertIsNotNone(duct.connections)
        self.assertEqual(duct.connections, principal_duct_conn)
        self.assertEqual(duct.connections.get_destination_entities(), [supply_air_duct])
        self.assertEqual(duct.connections.get_destination_entities()[0].connections.get_destination_entities(),
                         [self.floor])
        self.assertEqual(duct.connections.get_source_entities(), [return_air_duct])
        self.assertEqual(duct.connections.get_source_entities()[0].connections.get_source_entities(),
                         [self.floor, self.room])
        self.assertEqual(supply_air_duct.connections.get_source_entities(), [duct])






