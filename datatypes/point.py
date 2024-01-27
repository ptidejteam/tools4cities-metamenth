from dataclasses import dataclass


@dataclass
class Point:
    """
    A geo-coordinate point with latitude and longitude.

    Author: Peter Yefi
    Email: peteryefi@gmail.com
    """
    latitude: float
    longitude: float
