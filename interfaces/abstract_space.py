from abc import ABC
from abc import abstractmethod
import uuid
from datatypes import BinaryMeasure
from misc import Validate
from typing import Type


class AbstractSpace(ABC):
    """
    An abstract class for spaces in a building
    """

    def __init__(self, area: Type[BinaryMeasure], location: str = None):
        """
        :param area: The area of the space.
        :param location: The location of the space (three words delimited with two periods).
        """
        self.UID = uuid.uuid4()
        self.area = area
        self.location = Validate.validate_what3word(location)
        self.zones = []

    @abstractmethod
    def add_zone(self, zone):
        from datatypes import Zone # done to avoid circular import
        if isinstance(zone, Zone):
            self.zones.append(zone)
        else:
            raise("{0} is not an instance of Zone".format(zone))

