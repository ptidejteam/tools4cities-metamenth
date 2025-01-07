from uuid import uuid4
from metamenth.enumerations import BuildingType
from metamenth.datatypes.address import Address
from typing import List
from .floor import Floor
from .room import Room
from .open_space import OpenSpace
from .envelope import Envelope
from typing import Optional
from metamenth.measure_instruments.weather_station import WeatherStation
from metamenth.measure_instruments.meter import Meter
from metamenth.measure_instruments.interfaces.abstract_reader import AbstractReader
from metamenth.utils import EntityRemover
from metamenth.utils import EntityInsert
from metamenth.enumerations import BuildingEntity
from metamenth.datatypes.interfaces.abstract_measure import AbstractMeasure
from metamenth.virtual.zone import Zone
from metamenth.utils import StructureSearch
from typing import Dict
from metamenth.enumerations import RoomType
from metamenth.enumerations import OpenSpaceType
from metamenth.enumerations import TerrainType
from metamenth.enumerations import SolarDistributionType
from metamenth.observers.observable import Observable
from metamenth.misc import StateTrackDecorator
from metamenth.utils import StructureEntitySearch
from metamenth.enumerations import MeterType
from metamenth.subsystem.building_control_system import BuildingControlSystem
from metamenth.datatypes.schedulable_entity import SchedulableEntity


class Building(Observable):
    """
    A representation of a building

    Author: Peter Yefi
    Email: peteryefi@gmail.com
    """

    def __init__(self, construction_year: int, height: AbstractMeasure, floor_area: AbstractMeasure,
                 internal_mass: AbstractMeasure, address: Address, building_type: BuildingType, floors: List[Floor]):
        """
        :param construction_year: The construction year of the building
        :param height: The height of the building
        :param floor_area: The floor area of the building
        :param internal_mass: The internal mass of the building
        :param address: The address of the building
        :param building_type: The type of building
        """
        super().__init__()
        self._UID = str(uuid4())
        self._name = None
        self._construction_year = None
        self._height = None
        self._floor_area = None
        self._internal_mass = None
        self._address = None
        self._building_type = None
        self._terrain = None
        self._solar_distribution = None
        self._schedulable_entity = SchedulableEntity()
        self._envelope: [Envelope] = []  # multiple envelopes indicate multiple towers of a building
        self._floors = []
        self._meters: [AbstractReader] = []
        self._weather_stations: List[WeatherStation] = []
        self._zones: List[Zone] = []
        self._control_systems: [BuildingControlSystem] = []
        self.track_state = False

        # apply validation
        self.construction_year = construction_year
        self.height = height
        self.floor_area = floor_area
        self.internal_mass = internal_mass
        self.address = address
        self.building_type = building_type
        self.add_floors(floors)

    @property
    def UID(self) -> str:
        return self._UID

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def construction_year(self) -> int:
        return self._construction_year

    @construction_year.setter
    def construction_year(self, value):
        if value is not None:
            self._construction_year = value
        else:
            raise ValueError("construction_year must be a number")

    @property
    def height(self) -> AbstractMeasure:
        return self._height

    @height.setter
    def height(self, value: AbstractMeasure):
        if value is not None:
            self._height = value
        else:
            raise ValueError("height must be of type AbstractMeasure")

    @property
    def floor_area(self) -> AbstractMeasure:
        return self._floor_area

    @floor_area.setter
    @StateTrackDecorator
    def floor_area(self, value: AbstractMeasure):
        if value is not None:
            # write state before updating
            self._floor_area = value
        else:
            raise ValueError("floor_area must be of type AbstractMeasure")

    @property
    def internal_mass(self) -> AbstractMeasure:
        return self._internal_mass

    @internal_mass.setter
    def internal_mass(self, value: AbstractMeasure):
        if value is not None:
            self._internal_mass = value
        else:
            raise ValueError("internal_mass must be of type AbstractMeasure")

    @property
    def address(self) -> Address:
        return self._address

    @address.setter
    @StateTrackDecorator
    def address(self, value: Address):
        if value is not None:
            self._address = value
        else:
            raise ValueError("address must be of type Address")

    @property
    def building_type(self) -> BuildingType:
        return self._building_type

    @building_type.setter
    @StateTrackDecorator
    def building_type(self, value: BuildingType):
        if value is not None:
            self._building_type = value
        else:
            raise ValueError("building_type must be of type BuildingType")

    @property
    def floors(self):
        raise AttributeError("Cannot get floors")

    @floors.setter
    def floors(self, value: List[Floor]):
        if value is not None and len(value) > 0:
            self._floors = value
        else:
            raise ValueError("floors must be of type [Floor] and must not be empty")

    @property
    def weather_stations(self):
        raise AttributeError("Cannot get weather stations")

    @weather_stations.setter
    def weather_stations(self, value: List[WeatherStation]):
        if value is not None:
            self._weather_stations = value
        else:
            raise ValueError("weather_stations must be of type [WeatherStation]")

    @property
    def meters(self):
        raise AttributeError("Cannot get meters")

    @meters.setter
    def meters(self, value: List[AbstractReader]):
        if value is not None:
            self._meters = value
        else:
            raise ValueError("meters must be of type [Meter]")

    @property
    def envelope(self) -> [Envelope]:
        return self._envelope

    @StateTrackDecorator
    def add_envelope(self, value: Envelope):
        if value is not None:
            self._envelope.append(value)
        else:
            raise ValueError("envelope must be of type Envelope")

    @property
    def schedules(self):
        raise AttributeError("Cannot get schedules")

    @property
    def zones(self):
        return self._zones

    @zones.setter
    def zones(self, value):
        if value is not None:
            self._zones = value
        else:
            raise ValueError('zones must be of type [Zone]')

    @property
    def control_systems(self):
        return self._control_systems.copy()

    def add_control_system(self, control_system: BuildingControlSystem):
        if control_system:
            self._control_systems.append(control_system)

    @property
    def schedulable_entity(self) -> SchedulableEntity:
        return self._schedulable_entity

    @schedulable_entity.setter
    def schedulable_entity(self, value: SchedulableEntity):
        if value is None:
            raise ValueError("schedules should be of type SchedulableEntity")
        self._schedulable_entity = value

    @property
    def terrain(self) -> TerrainType:
        return self._terrain

    @terrain.setter
    def terrain(self, value: TerrainType):
        if value is not None:
            self._terrain = value
        else:
            raise ValueError("terrain must be of type TerrainType")

    @property
    def solar_distribution(self) -> SolarDistributionType:
        return self._solar_distribution

    @solar_distribution.setter
    def solar_distribution(self, value: SolarDistributionType):
        if value is not None:
            self._solar_distribution = value
        else:
            raise ValueError("solar_distribution must be of type SolarDistributionType")

    @StateTrackDecorator
    def add_weather_station(self, weather_station: WeatherStation):
        """
        Adds a weather station to a building
        :param weather_station: a station to measure various weather elements
        :return:
        """
        EntityInsert.insert_building_entity(self._weather_stations, weather_station)
        return self

    @StateTrackDecorator
    def remove_weather_station(self, weather_station: WeatherStation):
        """
        Adds a weather station to a building
        :param weather_station: a station to measure various weather elements
        :return:
        """
        EntityRemover.remove_building_entity(self._weather_stations, weather_station)

    def add_meter(self, meter: AbstractReader):
        """
        Adds a meter to a building
        :param meter: a meter to measure some phenomena e.g. energy consumption
        :return:
        """
        EntityInsert.insert_building_entity(self._meters, meter)
        return self

    def remove_meter(self, meter: AbstractReader):
        """
        Adds a meter to a building
        :param meter: a meter to measure some phenomena e.g. energy consumption
        :return:
        """
        EntityRemover.remove_building_entity(self._meters, meter)

    def add_floors(self, floors: List[Floor]):
        """
        Add multiple unique (by floor number) floors to a building
        :param floors: the floors to add to this building
        :return:
        """
        EntityInsert.insert_building_entity(self._floors, floors, BuildingEntity.FLOOR_SPACE.value)
        return self  # necessary for method chaining

    def remove_floor(self, floor: Floor):
        """
        Removes floor from a building
        :param floor: the floor to remove
        :return:
        """
        EntityRemover.remove_building_entity(self._floors, floor)

    def get_floor_by_uid(self, uid: str) -> Floor:
        """
        Retrieves a floor given the uid
        :param uid: the uid of the floor
        :return:
        """
        return StructureSearch.search_by_id(self._floors, uid)

    def get_floor_by_number(self, floor_number: int) -> Floor:
        """
        Retrieves a floor given the floor number
        :param floor_number: the number assigned to the floor
        :return:
        """
        return StructureSearch.search_by_number(self._floors, floor_number)

    def get_floors(self, search_term: Dict = None) -> List[Floor]:
        """
        Retrieves floors given the attributes and their values
        :param search_term: the uid of the floor
        :return:
        """
        return StructureSearch.search(self._floors, search_term)

    def get_weather_station_by_name(self, name: str) -> WeatherStation:
        """
        Returns a weather station
        :param name: the name of the weather station
        :return:
        """
        return StructureEntitySearch.search_by_name(self._weather_stations, name)

    def get_weather_station_by_uid(self, uid: str) -> WeatherStation:
        """
        Returns a weather station
        :param uid: the unique identifier of the weather station
        :return:
        """
        return StructureEntitySearch.search_by_id(self._weather_stations, uid)

    def get_weather_stations(self, search_term: Dict = None) -> [WeatherStation]:
        """
        Returns a list of weather stations
        :param search_term: attributes and their values
        :return:
        """
        return StructureEntitySearch.search(self._weather_stations, search_term)

    def get_meter_by_uid(self, uid: str) -> AbstractReader:
        """
        Returns a meter based on uid
        :param uid: the uid of the meter
        :return:
        """
        return StructureEntitySearch.search_by_id(self._meters, uid)

    def get_meter_by_type(self, meter_type: MeterType) -> [Meter]:
        """
        Returns a meter based on type of meter
        :param meter_type: the type of meter
        :return:
        """
        return StructureEntitySearch.search(self._meters, {'meter_type': meter_type})

    def get_meters(self, search_terms: Dict = None) -> [AbstractReader]:
        """
        Returns a meter based on some attributes and their values
        :param search_terms: attributes and value key pairs
        :return:
        """
        return StructureEntitySearch.search(self._meters, search_terms)

    def get_zone_by_name(self, name) -> Zone:
        """
        Search zones by name
        :param name:  the name of the zone
        :return:
        """
        return StructureEntitySearch.search_by_name(self._zones, name)

    def get_zone_by_uid(self, uid) -> Zone:
        """
        Search zones by uid
        :param uid: the unique identifier of the overlapping zone
        :return:
        """
        return StructureEntitySearch.search_by_id(self._zones, uid)

    def get_zones(self, search_terms: Dict = None) -> [Zone]:
        """
        Search zones by attributes values
        :param search_terms: a dictionary of attributes and their values
        :return:
        """
        return StructureEntitySearch.search(self._zones, search_terms)

    @StateTrackDecorator
    def add_room(self, floor_uid: str, name: str, area: AbstractMeasure,
                 room_type: RoomType,
                 location: str = None):
        """
        Adds a room to a building's floor
        :param floor_uid: the unique ID of the floor
        :param area: the area of the room
        :param name: the name of the room
        :param room_type: the tupe of room
        :param location: the location of the room
        :return:
        """
        if not self.get_floor_by_uid(floor_uid):
            raise ValueError("Cannot add room without a floor")
        self.get_floor_by_uid(floor_uid).add_rooms([Room(area, name, room_type, location)])
        return self  # Return self for method chaining

    @StateTrackDecorator
    def add_open_space(self, floor_uid: str, name: str, area: AbstractMeasure,
                       space_type: OpenSpaceType, location: str = None):
        """
        Adds an open space to a building's floor
        :param floor_uid: the floor UID
        :param name: the name of the open space
        :param area: the area of the open space
        :param space_type: the type of open space
        :param location: the location of the open space
        :return:
        """
        if not self.get_floor_by_uid(floor_uid):
            raise ValueError("Cannot add open space without a floor")
        self.get_floor_by_uid(floor_uid).add_open_spaces([OpenSpace(name, area, space_type, location)])
        return self  # Return self for method chaining

    def accept(self, visitor):
        """
        visitor method to accept
        visit operation to building floors
        :param visitor: the visitor object
        """
        visitor.visit_building(self)

    def __str__(self):
        floors_info = "\n".join([f"  - Floor {floor.number}: {floor}" for floor in self._floors])
        weather_stations_info = "\n".join([f"  - {station}" for station in self._weather_stations])
        schedules_info = "\n".join([f"  - {schedule}" for schedule in self._schedulable_entity.get_schedules()])
        meter_info = "\n".join([f"  - {meter}" for meter in self._meters])

        return (f"Building("
                f"UID: {self.UID}, "
                f"Construction Year: {self.construction_year}, "
                f"Height: {self.height}, "
                f"Floor Area: {self.floor_area}, "
                f"Internal Mass: {self.internal_mass}, "
                f"Address: {self.address}, "
                f"Building Type: {self.building_type}, "
                f"Terrain: {self.terrain}, "
                f"Solar Distribution: {self.solar_distribution}, "
                f"Floor Count: {len(self._floors)}, "
                f"Weather Stations Count: {len(self._weather_stations)}, "
                f"Schedules: {len(self._schedulable_entity.get_schedules())}, "
                f"Floors:\n{floors_info}, "
                f"Weather Stations:\n{weather_stations_info}, "
                f"Schedules:\n{schedules_info}, "
                f"Meters:\n{meter_info}, "
                f"Envelope: {self.envelope}")
