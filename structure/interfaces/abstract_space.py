from abc import ABC
import uuid
from datatypes.interfaces.abstract_measure import AbstractMeasure
from misc import Validate


class AbstractSpace(ABC):
    """
    An abstract class for spaces in a building
    """

    def __init__(self, area: AbstractMeasure, location: str = None):
        """
        :param area: The area of the space.
        :param location: The location of the space (three words delimited with two periods).
        """
        self._UID = str(uuid.uuid4())
        self._area = None
        self._location = None
        self._zones = []

        # Apply validation
        self.area = area
        self.location = location

    @property
    def UID(self) -> str:
        return self._UID

    @property
    def area(self) -> AbstractMeasure:
        return self._area

    @area.setter
    def area(self, value: AbstractMeasure):
        if value is None:
            raise ValueError('area must be of type BinaryMeasure')
        self._area = value

    @property
    def location(self) -> str:
        return self._location

    @location.setter
    def location(self, value: str):
        self._location = Validate.validate_what3word(value)

    @property
    def zones(self):
        return self._zones

    def add_zone(self, zone):
        from datatypes.zone import Zone
        if isinstance(zone, Zone):
            self.zones.append(zone)

    def __str__(self):
        return (
            f"UID: {self.UID}, "
            f"Area: {self.area}, "
            f"Location: {self.location}, "
            f"Zones: {self.zones}, "
        )


