from metamenth.datatypes.point import Point
from metamenth.datatypes.binary_measure import BinaryMeasure
from metamenth.misc import Validate


class Address:
    """
    Address of a building

    Author: Peter Yefi
    Email: peteryefi@gmail.com
    """
    def __init__(self, city: str, street: str, state: str, zip_code: str, country: str,
                 geocoordinate: Point = None,  what3word: str = None, north_orientation: BinaryMeasure = None):
        """
        :param city: The name of the city
        :param street: The street e.g., 6911 Ave De la Pepiniere.
        :param state: The state (or province) e.g., QC or Quebec.
        :param zip_code: The ZIP code e.g., H1N 1B9
        :param country: the country where the building is located
        :param what3word: The What3word address of the location.
        :param geocoordinate: The geographical coordinates of the location (an instance of Point).
        :param north_orientation: The north orientation of a building.
        """
        self.city = city
        self.street = street
        self.state = state
        self.zip_code = zip_code
        self.country = country
        self.what3word = Validate.validate_what3word(what3word)
        self.geocoordinate = geocoordinate
        self.north_orientation = north_orientation

    def __str__(self):
        geo_coordinate_str = (
            f", GeoCoordinate: (Latitude: {self.geocoordinate.latitude}, Longitude: {self.geocoordinate.longitude})"
            if self.geocoordinate is not None
            else None
        )

        north_orientation_str = (
            f", North Orientation: {self.north_orientation.value}"
            if self.north_orientation is not None
            else None
        )

        return (
            f"GeoLocation("
            f"City: {self.city}, "
            f"Street: {self.street}, "
            f"State: {self.state}, "
            f"ZIP Code: {self.zip_code}, "
            f"Country: {self.country}, "
            f"What3word: {self.what3word}"
            f"{geo_coordinate_str}"
            f"{north_orientation_str})"
        )

