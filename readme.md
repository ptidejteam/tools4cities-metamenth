# MetamEnTh

![Build Status](https://github.com/peteryefi/metamenth/actions/workflows/build.yml/badge.svg)
![Version](https://img.shields.io/badge/version-1.0.0-blue)
[![License](https://img.shields.io/github/license/peteryefi/metamenth)](https://github.com/username/repository/blob/main/LICENSE)
![PyPI version](https://img.shields.io/pypi/v/metamenth.svg)
[![Wiki](https://img.shields.io/badge/docs-wiki-blue.svg)](https://github.com/peteryefi/metamenth/wiki)

Read the documentation here: [MetamEnTh Documentation](https://github.com/peteryefi/metamenth/wiki)

### Setting up MetamEnTh Locally

1. Clone the GitHub repository:

   ```sh
   git clone https://github.com/peteryefi/metamenth.git
   cd metamenth
   
2. Create a virtual environment
    ```sh
    python3 -m venv venv
   
3. Activate the virtual environment
    * Windows
        ```sh
        venv\Scripts\activate
    * MacOS/Linux
        ```sh
        source venv/bin/activate
  
4. Install project dependencies
    ```sh
    pip install -r requirements.txt
   
5. Run the tests
    ```sh
     chmod +x run_tests.sh
     ./run_tests.sh

### Example usage
```python
from unittest import TestCase
from misc import MeasureFactory
from enumerations import RecordingType
from datatypes.measure import Measure
from enumerations import MeasurementUnit
from structure.open_space import OpenSpace
from enumerations import OpenSpaceType
from enumerations import RoomType
from structure.room import Room
from structure.floor import Floor
from enumerations import FloorType
from structure.building import Building
from enumerations import BuildingType
from datatypes.address import Address
from structure.layer import Layer
from structure.material import Material
from enumerations import MaterialType
from enumerations import LayerRoughness
from structure.cover import Cover
from structure.envelope import Envelope
from enumerations import CoverType

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
building.envelope = envelope
```
NB: Refer to the [test directory](https://github.com/peteryefi/metamenth/tree/main/tests) for more insight on usage