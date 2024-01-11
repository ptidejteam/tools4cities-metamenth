from abc import ABC
import uuid
from datatypes import BinaryMeasure


class AbstractSpace(ABC):
    """An abstract class representing building and related spaces"""

    def __init__(self, area: BinaryMeasure, location: str):
        """
        Initializes an AbstractSpace instance.

        Parameters:
        - area (BinaryMeasure): The area of the space.
        - location (str): The location of the space (three words delimited with two periods).
        """
        self.UID = uuid.uuid4()
        self.area = area
        self.location = self._validate_location(location)

    def _validate_location(self, location: str) -> str:
        """
        Validates and ensures location is in what3word format: word.word.word.

        Parameters:
        - location (str): The raw location string.

        Returns:
        str: The validated and formatted location string.
        """
        words = location.strip().split()
        if len(words) == 3 and all(word.endswith('.') for word in words):
            return location.strip()
        else:
            raise ValueError("Location should be a string of three words delimited with two periods.")
