from uuid import uuid4
from enumerations import BuildingType
from datatypes.address import Address
from datatypes.operational_schedule import OperationalSchedule
from typing import List
from .floor import Floor
from .room import Room
from .open_space import OpenSpace
from .envelope import Envelope
from typing import Optional
from measure_instruments import WeatherStation
from measure_instruments import Meter
from visitors import EntityRemover
from visitors import EntityInsert
from enumerations import BuildingEntity
from datatypes.interfaces.abstract_measure import AbstractMeasure
from datatypes.zone import Zone
from visitors import StructureSearch
from typing import Dict
from enumerations import RoomType
from enumerations import OpenSpaceType


class Building:
    """
    A representation of a building

    Author: Peter Yefi
    Email: peteryefi@gmail.com
    """
    def __init__(
        self,
        construction_year: int,
        height: AbstractMeasure,
        floor_area: AbstractMeasure,
        internal_mass: AbstractMeasure,
        address: Address,
        building_type: BuildingType,
        floors: List[Floor]
    ):
        """
        :param construction_year: The construction year of the building
        :param height: The height of the building
        :param floor_area: The floor area of the building
        :param internal_mass: The internal mass of the building
        :param address: The address of the building
        :param building_type: The type of building
        """
        self._UID = str(uuid4())
        self._construction_year = None
        self._height = None
        self._floor_area = None
        self._internal_mass = None
        self._address = None
        self._building_type = None
        self._schedules: List[OperationalSchedule] = []
        self._envelope: Envelope = Optional[None]
        self._floors = None
        self._meters: [Meter] = []
        self._weather_stations: List[WeatherStation] = []
        self._zones: List[Zone] = []

        # apply validation
        self.construction_year = construction_year
        self.height = height
        self.floor_area = floor_area
        self.internal_mass = internal_mass
        self.address = address
        self.building_type = building_type
        self.floors = floors

    @property
    def UID(self) -> str:
        return self._UID

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
    def floor_area(self, value: AbstractMeasure):
        if value is not None:
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
    def address(self, value: Address):
        if value is not None:
            self._address = value
        else:
            raise ValueError("address must be of type Address")

    @property
    def building_type(self) -> BuildingType:
        return self._building_type

    @building_type.setter
    def building_type(self, value: BuildingType):
        if value is not None:
            self._building_type = value
        else:
            raise ValueError("building_type must be of type BuildingType")

    @property
    def floors(self) -> List[Floor]:
        return self._floors

    @floors.setter
    def floors(self, value: List[Floor]):
        if value is not None and len(value) > 0:
            self._floors = value
        else:
            raise ValueError("floors must be of type [Floor] and must not be empty")

    @property
    def weather_stations(self) -> List[WeatherStation]:
        return self._weather_stations

    @weather_stations.setter
    def weather_stations(self, value: List[WeatherStation]):
        if value is not None:
            self._weather_stations = value
        else:
            raise ValueError("weather_stations must be of type [WeatherStation]")

    @property
    def meters(self) -> List[Meter]:
        return self._meters

    @meters.setter
    def meters(self, value: List[Meter]):
        if value is not None:
            self._meters = value
        else:
            raise ValueError("meters must be of type [WeatherStation]")

    @property
    def envelope(self) -> Envelope:
        return self._envelope

    @envelope.setter
    def envelope(self, value: Envelope):
        if value is not None:
            self._envelope = value
        else:
            raise ValueError("envelope must be of type Envelope")

    @property
    def schedules(self) -> List[OperationalSchedule]:
        return self._schedules

    @property
    def zones(self):
        return self._zones

    @zones.setter
    def zones(self, value):
        if value is not None:
            self._zones = value
        else:
            raise ValueError('zones must be of type [Zone]')

    def add_weather_station(self, weather_station: WeatherStation):
        """
        Adds a weather station to a building
        :param weather_station: a station to measure various weather elements
        :return:
        """
        self.weather_stations.append(weather_station)
        return self

    def remove_weather_station(self, weather_station: WeatherStation):
        """
        Adds a weather station to a building
        :param weather_station: a station to measure various weather elements
        :return:
        """
        EntityRemover.remove_building_entity(self, BuildingEntity.WEATHER_STATION.value, weather_station)

    def add_meter(self, meter: Meter):
        """
        Adds a meter to a building
        :param meter: a meter to measure some phenomena e.g. energy consumption
        :return:
        """
        self.meters.append(meter)
        return self

    def remove_meter(self, meter: Meter):
        """
        Adds a meter to a building
        :param meter: a meter to measure some phenomena e.g. energy consumption
        :return:
        """
        EntityRemover.remove_building_entity(self, BuildingEntity.METER.value, meter)

    def add_schedule(self, schedule: OperationalSchedule):
        """
        Adds an operational schedule to this building
        :param schedule: the schedule
        :return:
        """
        EntityInsert.insert_space_entity(self, schedule, BuildingEntity.SCHEDULE.value)
        return self

    def remove_schedule(self, schedule: OperationalSchedule):
        """
        Removes an operational schedule from this building
        :param schedule: the schedule
        :return:
        """
        EntityRemover.remove_space_entity(self, BuildingEntity.SCHEDULE.value, schedule)

    def add_floors(self, floors: List[Floor]):
        """
        Add multiple unique (by floor number) floors to a building
        :param floors: the floors to add to this building
        :return:
        """
        for new_floor in floors:
            existing_floor = next((floor for floor in self.floors if floor.number == new_floor.number), None)
            if existing_floor is None:
                self.floors.append(new_floor)
        return self # necessary for method chaining

    def remove_floor(self, floor: Floor):
        """
        Removes floor from a building
        :param floor: the floor to remove
        :return:
        """
        EntityRemover.remove_building_entity(self, BuildingEntity.FLOOR.value, floor)

    def get_floor_by_uid(self, uid: str) -> Floor:
        """
        Retrieves a floor given the uid
        :param uid: the uid of the floor
        :return:
        """
        return StructureSearch.search_by_id(self.floors, uid)

    def get_floor_by_number(self, floor_number: int) -> Floor:
        """
        Retrieves a floor given the floor number
        :param floor_number: the number assigned to the floor
        :return:
        """
        return StructureSearch.search_by_number(self.floors, floor_number)

    def get_floors(self, search_term: Dict) -> List[Floor]:
        """
        Retrieves floors given the attributes and their values
        :param search_term: the uid of the floor
        :return:
        """
        return StructureSearch.search(self.floors, search_term)

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

    def __str__(self):
        floors_info = "\n".join([f"  - Floor {floor.number}: {floor}" for floor in self.floors])
        weather_stations_info = "\n".join([f"  - {station}" for station in self.weather_stations])
        schedules_info = "\n".join([f"  - {schedule}" for schedule in self.schedules])
        meter_info = "\n".join([f"  - {meter}" for meter in self.meters])

        return (f"Building("
                f"UID: {self.UID}, "
                f"Construction Year: {self.construction_year}, "
                f"Height: {self.height}, "
                f"Floor Area: {self.floor_area}, "
                f"Internal Mass: {self.internal_mass}, "
                f"Address: {self.address}, "
                f"Building Type: {self.building_type}, "
                f"Floor Count: {len(self.floors)}, "
                f"Weather Stations Count: {len(self.weather_stations)}, "
                f"Schedules Count: {len(self.schedules)}, "
                f"Floors:\n{floors_info}, "
                f"Weather Stations:\n{weather_stations_info}, "
                f"Schedules:\n{schedules_info}, "
                f"Meters:\n{meter_info}, "
                f"Envelope: {self.envelope}")
