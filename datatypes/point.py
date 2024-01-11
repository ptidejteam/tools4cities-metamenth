class Point:
    """
    A geo-coordinate point with latitude and longitude.

    Author: Peter Yefi
    Email: peteryefi@gmail.com
    """

    def __init__(self, latitude: float, longitude: float):
        """
        Parameters:
        - latitude (float): The latitude coordinate.
        - longitude (float): The longitude coordinate.
        """
        self.latitude = latitude
        self.longitude = longitude

    def __str__(self):
        return f"Latitude: {self.latitude}, Longitude: {self.longitude}"
