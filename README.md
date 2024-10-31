# Metamodel for Energy Things (MetamEnTh)

![Build Status](https://github.com/ptidejteam/metamenth/actions/workflows/build.yml/badge.svg)
![Version](https://img.shields.io/badge/version-1.0.0-blue)
[![License](https://img.shields.io/github/license/ptidejteam/metamenth)](https://github.com/ptidejteam/metamenth/blob/main/LICENSE)
![PyPI version](https://img.shields.io/pypi/v/metamenth.svg)
[![Wiki](https://img.shields.io/badge/docs-wiki-blue.svg)](https://github.com/ptidejteam/metamenth/wiki)

**MetamEnTh** is an object-oriented framework for modeling the operational aspects of buildings, with a focus on mechanical, electrical, and plumbing (MEP) entities. It allows users to model and interact with physical structures, such as rooms, floors, HVAC systems, and appliances, providing a detailed simulation of building components and energy systems.

Read the documentation here: [MetamEnTh Documentation](https://github.com/ptidejteam/metamenth/wiki)

## Table of Contents
1. [Setting up MetamEnTh Locally](#setting-up-metamEnTh-locally)
   - [Cloning the repository](#cloning-the-repository)
   - [Creating a virtual environment](#creating-a-virtual-environment)
   - [Activate the virtual environment](#activating-the-virtual-environment)
   - [Installing dependencies](#installing-dependencies)
   - [Running tests](#running-tests)
3. [Example Usage](#example-usage)


## Setting up MetamEnTh Locally

### Cloning the repository:

   ```sh
   git clone https://github.com/ptidejteam/metamenth.git
   cd metamenth
   ```
   
### Creating a virtual environment
```shell
python3 -m venv venv
```
   
   
### Activating the virtual environment

```shell
# Windows
venv\Scripts\activate

# MacOS/Linux
source venv/bin/activate
```

### Installing dependencies
```shell
pip install -r requirements.txt
```
   
### Running tests
```shell
chmod +x run_tests.sh
     ./run_tests.sh
```

## Example usage

### 1. Creating the Building

```python
from metamenth.misc import MeasureFactory
from metamenth.enumerations import RecordingType
from metamenth.datatypes.measure import Measure
from metamenth.enumerations import MeasurementUnit
from metamenth.structure.open_space import OpenSpace
from metamenth.enumerations import OpenSpaceType
from metamenth.enumerations import RoomType
from metamenth.structure.room import Room
from metamenth.structure.floor import Floor
from metamenth.enumerations import FloorType
from metamenth.structure.building import Building
from metamenth.enumerations import BuildingType
from metamenth.datatypes.address import Address

floor_area = MeasureFactory.create_measure(RecordingType.BINARY.value,
                                           Measure(MeasurementUnit.SQUARE_METERS, 5))
# height of building
height = MeasureFactory.create_measure(RecordingType.BINARY.value,
                                       Measure(MeasurementUnit.METERS, 30))
# internal mass of the building
internal_mass = MeasureFactory.create_measure(RecordingType.BINARY.value,
                                              Measure(MeasurementUnit.KILOGRAMS, 2000))
area = MeasureFactory.create_measure(RecordingType.BINARY.value,
                                     Measure(MeasurementUnit.SQUARE_METERS, 45))
# create room
room = Room(area, "Office 1", RoomType.OFFICE)

mechanical_room = Room(area, "MR 01", RoomType.MECHANICAL)

# create a hall
hall = OpenSpace("Hall", area, OpenSpaceType.HALL)

# create a corridor
corridor = OpenSpace("Corridor", area, OpenSpaceType.CORRIDOR)

# create floor with a room and a hall
floor = Floor(area=area, number=1, floor_type=FloorType.REGULAR, rooms=[room, hall, corridor, mechanical_room])

# create the building's address
address = Address("Montreal", "6399 Rue Sherbrooke", "QC", "H1N 2Z3", "Canada")

# create building
building = Building(2009, height, floor_area, internal_mass, address,
                    BuildingType.COMMERCIAL, [floor])
```
### 2. Adding an envelope with roof
```python
from metamenth.structure.layer import Layer
from metamenth.structure.material import Material
from metamenth.enumerations import MaterialType
from metamenth.enumerations import LayerRoughness
from metamenth.structure.cover import Cover
from metamenth.structure.envelope import Envelope
from metamenth.enumerations import CoverType
from metamenth.enumerations import RecordingType
from metamenth.datatypes.measure import Measure
from metamenth.enumerations import MeasurementUnit
from metamenth.misc import MeasureFactory

# material properties
density_measure = MeasureFactory.create_measure(RecordingType.BINARY.value,
                                                Measure(MeasurementUnit.KILOGRAM_PER_CUBIC_METER, 0.5))
hc_measure = MeasureFactory.create_measure(RecordingType.BINARY.value,
                                           Measure(MeasurementUnit.JOULES_PER_KELVIN, 4.5))
tt_measure = MeasureFactory.create_measure(RecordingType.BINARY.value,
                                           Measure(MeasurementUnit.WATTS_PER_SQUARE_METER_KELVIN, 2.5))
tr_measure = MeasureFactory.create_measure(RecordingType.BINARY.value,
                                           Measure(MeasurementUnit.SQUARE_METERS_KELVIN_PER_WATTS,
                                                   2.3))

# create roof material
roof_material = Material(
   description="Steel roof",
   material_type=MaterialType.ROOF_STEEL,
   density=density_measure,
   heat_capacity=hc_measure,
   thermal_transmittance=tt_measure,
   thermal_resistance=tr_measure
)

# roof layer measurement
roof_height = MeasureFactory.create_measure(RecordingType.BINARY.value, Measure(MeasurementUnit.METERS, 20))
roof_length = MeasureFactory.create_measure(RecordingType.BINARY.value, Measure(MeasurementUnit.METERS, 15))
roof_width = MeasureFactory.create_measure(RecordingType.BINARY.value, Measure(MeasurementUnit.METERS, 3))
# create a layer of steel roof
roof_layer = Layer(roof_height, roof_length, roof_width, roof_material, LayerRoughness.MEDIUM_ROUGH)

# create a cover for the roof
roof_cover = Cover(CoverType.FLOOR)

# roof layer to cover
roof_cover.add_layer(roof_layer)

# create building envelope and add roof cover
envelope = Envelope()
envelope.add_cover(roof_cover)
building.envelope = envelope # building was created 1 above
```

### 3. Create and associate zones to the hall, corridor, room and office
```python
from metamenth.enumerations import ZoneType
from metamenth.enumerations import HVACType
from metamenth.virtual.zone import Zone

hvac_zone_1 = Zone("HVAC Zone 1", ZoneType.HVAC, HVACType.INTERIOR)
hvac_zone_2 = Zone("HVAC Zone 2", ZoneType.HVAC, HVACType.INTERIOR)
# set adjacent zones
hvac_zone_2.add_adjacent_zones([hvac_zone_1])

# assign the mechanical room to hvac zone 1
mechanical_room.add_zone(hvac_zone_1, building) # building and mechanical room were created in 1 above

# assign the hall, corridor and room to hvac zone 2
room.add_zone(hvac_zone_2, building)
corridor.add_zone(hvac_zone_2, building)
hall.add_zone(hvac_zone_2, building)

```
### 4. Create and assign thermostat to the hall
```python
from metamenth.transducers.sensor import Sensor
from metamenth.subsystem.appliance import Appliance
from metamenth.enumerations import ApplianceType
from metamenth.enumerations import ApplianceCategory
from metamenth.enumerations import SensorMeasureType
from metamenth.enumerations import SensorMeasure
from metamenth.enumerations import SensorLogType
from metamenth.datatypes.measure import Measure
from metamenth.enumerations import MeasurementUnit
from metamenth.misc import MeasureFactory

temp_op_condition = MeasureFactory.create_measure("Continuous",
                                    Measure(MeasurementUnit.DEGREE_CELSIUS, 4.4, 37.8))
humidity_op_conditions = MeasureFactory.create_measure("Continuous",
                                    Measure(MeasurementUnit.RELATIVE_HUMIDITY, 20, 80))
thermostat = Appliance("Thermostat", [ApplianceCategory.HOME, ApplianceCategory.SMART],
                               ApplianceType.THERMOSTAT,
                               operating_conditions=[temp_op_condition, humidity_op_conditions])

# create three sensors and assign them to the room
presence_sensor = Sensor("PRESENCE.SENSOR", SensorMeasure.OCCUPANCY, MeasurementUnit.PRESENCE,
                            SensorMeasureType.THERMO_COUPLE_TYPE_A, 0, sensor_log_type=SensorLogType.POLLING)
temp_sensor = Sensor("TEMPERATURE.SENSOR", SensorMeasure.TEMPERATURE, MeasurementUnit.DEGREE_CELSIUS,
                            SensorMeasureType.THERMO_COUPLE_TYPE_A, 900, sensor_log_type=SensorLogType.POLLING)
humidity_sensor = Sensor("HUMIDITY.SENSOR", SensorMeasure.HUMIDITY, MeasurementUnit.RELATIVE_HUMIDITY,
                            SensorMeasureType.THERMO_COUPLE_TYPE_A, 900, sensor_log_type=SensorLogType.POLLING)

thermostat.add_transducer(presence_sensor)
thermostat.add_transducer(temp_sensor)
thermostat.add_transducer(humidity_sensor)

# add thermostat to the hall
hall.add_appliance(thermostat) # hall was created in 1 above
```
#### 5. Create and assign sensors to the corridor, room and mechanical room
```python
from metamenth.transducers.sensor import Sensor
from metamenth.subsystem.appliance import Appliance
from metamenth.enumerations import ApplianceType
from metamenth.enumerations import ApplianceCategory
from metamenth.enumerations import SensorMeasureType
from metamenth.enumerations import SensorMeasure
from metamenth.enumerations import SensorLogType
from metamenth.datatypes.measure import Measure
from metamenth.enumerations import MeasurementUnit
from metamenth.misc import MeasureFactory

# room sensors
room_temp_sensor = Sensor("ROOM.TEMP.SENSOR", SensorMeasure.TEMPERATURE, MeasurementUnit.DEGREE_CELSIUS,
                            SensorMeasureType.THERMO_COUPLE_TYPE_A, 900, sensor_log_type=SensorLogType.POLLING)
room_co2_sensor = Sensor("ROOM.CO2.SENSOR", SensorMeasure.CARBON_DIOXIDE, MeasurementUnit.PARTS_PER_MILLION,
                            SensorMeasureType.THERMO_COUPLE_TYPE_A, 900, sensor_log_type=SensorLogType.POLLING)
room.add_transducer(room_co2_sensor)
room.add_transducer(room_temp_sensor)

# mechanical room sensors
mec_room_temp_sensor = Sensor("MEC.ROOM.TEMP.SENSOR", SensorMeasure.TEMPERATURE, MeasurementUnit.DEGREE_CELSIUS,
                            SensorMeasureType.THERMO_COUPLE_TYPE_B, 900, sensor_log_type=SensorLogType.CHANGE_OF_VALUE)
mec_room_humidity_sensor = Sensor("MEC.ROOM.HDT.SENSOR", SensorMeasure.HUMIDITY, MeasurementUnit.RELATIVE_HUMIDITY,
                            SensorMeasureType.THERMO_COUPLE_TYPE_A, 900, sensor_log_type=SensorLogType.POLLING)
mechanical_room.add_transducer(mec_room_humidity_sensor)
mechanical_room.add_transducer(mec_room_temp_sensor)

# add smoke detector to mechanical room
temp_op_condition = MeasureFactory.create_measure("Continuous",
                                    Measure(MeasurementUnit.DEGREE_CELSIUS, 0, 38))
humidity_op_condition = MeasureFactory.create_measure("Continuous",
                                    Measure(MeasurementUnit.RELATIVE_HUMIDITY, 0, 95))
smoke_detector = Appliance("SMK.DETECTOR", [ApplianceCategory.HOME, ApplianceCategory.SMART],
                               ApplianceType.SMOKE_DETECTOR,
                               operating_conditions=[temp_op_condition, humidity_op_condition])
mechanical_room.add_appliance(smoke_detector)

# corridor sensors
corr_room_temp_sensor = Sensor("CORR.ROOM.TEMP.SENSOR", SensorMeasure.TEMPERATURE, MeasurementUnit.DEGREE_CELSIUS,
                            SensorMeasureType.THERMO_COUPLE_TYPE_B, 900, sensor_log_type=SensorLogType.CHANGE_OF_VALUE)
corridor.add_transducer(corr_room_temp_sensor)
```
#### 6. Create and add the fan coil unit, baseboard heater, chiller and boiler
```python
from metamenth.subsystem.hvac_components.fan_coil_unit import FanCoilUnit
from metamenth.subsystem.hvac_components.heat_exchanger import HeatExchanger
from metamenth.subsystem.hvac_components.chiller import Chiller
from metamenth.subsystem.hvac_components.boiler import Boiler
from metamenth.subsystem.hvac_components.fan import Fan
from metamenth.enumerations import ChillerType, BoilerCategory, FCUType, FCUPipeSystem, PowerState 
from metamenth.enumerations import HeatingType, HeatExchangerType, HeatExchangerFlowType
from metamenth.subsystem.baseboard_heater import BaseboardHeater
from metamenth.subsystem.hvac_components.variable_frequency_drive import VariableFrequencyDrive

# create boiler and chiller and add them to mechanical room
boiler = Boiler('MEC.BOILER', BoilerCategory.NATURAL_GAS, PowerState.ON)
chiller = Chiller('MEC.CHILLER', ChillerType.WATER_COOLED, PowerState.ON)
mechanical_room.add_hvac_component(boiler)
mechanical_room.add_hvac_component(chiller)

# create baseboard heater add it to the corridor
baseboard_heater = BaseboardHeater('CORR.BS.HEATER', HeatingType.ELECTRIC, PowerState.OUT_OF_SERVICE)
corridor.add_hvac_component(baseboard_heater)

# create fan coil unit and add it to the hall
vfd = VariableFrequencyDrive('VFD')
fan = Fan("FCU.FAN", PowerState.ON, vfd)
heat_exchanger = HeatExchanger("FCU.HT.EXG", HeatExchangerType.FIN_TUBE, HeatExchangerFlowType.PARALLEL)
fcu = FanCoilUnit('HALL.FCU', heat_exchanger, fan, FCUType.STANDALONE, FCUPipeSystem.TWO_PIPE, False)
hall.add_hvac_component(fcu)
```
#### 7. Create an HVAC system for the building
```python
from metamenth.subsystem.building_control_system import BuildingControlSystem
from metamenth.subsystem.hvac_system import HVACSystem
from metamenth.subsystem.hvac_components.duct import Duct
from metamenth.enumerations import DuctType, DuctSubType
from metamenth.subsystem.hvac_components.duct_connection import DuctConnection
from metamenth.enumerations import DuctConnectionEntityType, VentilationType
from metamenth.subsystem.ventilation_system import VentilationSystem

bcs = BuildingControlSystem("EV Control System")
hvac_system = HVACSystem()
bcs.hvac_system = hvac_system

# Create the fresh air duct for the ventilation system
supply_air_duct = Duct("SUPP.VNT.01", DuctType.AIR)
supply_air_duct.duct_sub_type = DuctSubType.FRESH_AIR

# create the return air duct for the ventilation system
return_air_duct = Duct("RET.VNT.01", DuctType.AIR)
return_air_duct.duct_sub_type = DuctSubType.RETURN_AIR

# create the recirculation air duct
recirculation_air_duct = Duct("REC.VNT.01", DuctType.AIR)
recirculation_air_duct.duct_sub_type = DuctSubType.RETURN_AIR

# connect the fresh air, return air and recirculation air ducts
duct2duct_conn = DuctConnection()
# add the return air duct as the source of the connection
duct2duct_conn.add_entity(DuctConnectionEntityType.SOURCE, return_air_duct)
# add the fresh air duct as the destination of the connection
duct2duct_conn.add_entity(DuctConnectionEntityType.DESTINATION, supply_air_duct)
# set the connection object as a property of the recirculation air duct
recirculation_air_duct.connections = duct2duct_conn

# set the recirculation air duct as the source for the supply air duct
supp_duct_conn = DuctConnection()
supp_duct_conn.add_entity(DuctConnectionEntityType.SOURCE, recirculation_air_duct)
supply_air_duct.connections = duct2duct_conn

# create the ventilation system with the supply air duct as the principal duct
ventilation_system = VentilationSystem(VentilationType.AIR_HANDLING_UNIT, supply_air_duct)

# set the ventilation system for the HVAC system
hvac_system.add_ventilation_system(ventilation_system)
```


NB: Refer to the [test directory](https://github.com/ptidejteam/metamenth/tree/main/tests) for more insight on usage