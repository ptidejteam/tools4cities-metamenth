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
hall = OpenSpace("Dinning Hall", area, OpenSpaceType.HALL)

# create floor with a room and a hall
floor = Floor(area=area, number=1, floor_type=FloorType.REGULAR, rooms=[room, hall, mechanical_room])

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

### 3. Create and associate zones to the hall
```python
from metamenth.enumerations import ZoneType
from metamenth.enumerations import HVACType
from metamenth.virtual.zone import Zone

hvac_cooling_zone = Zone("HVAC_COOLING_ZONE", ZoneType.HVAC, HVACType.INTERIOR)
hvac_heating_zone = Zone("HVAC_HEATING_ZONE", ZoneType.HVAC, HVACType.PERIMETER)
# make the cooling zone adjacent to the heating zone
hvac_heating_zone.add_adjacent_zones([hvac_cooling_zone])

# assign the zone to the room
hall.add_zone(hvac_heating_zone, building) # building and hall were created in 1 above

```
### 4. Create and assign thermostats to the hall
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


NB: Refer to the [test directory](https://github.com/ptidejteam/metamenth/tree/main/tests) for more insight on usage