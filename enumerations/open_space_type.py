from enum import Enum


class OpenSpaceType(Enum):
    """
    Open spaces on floors of buildings

    Author: Peter Yefi
    Email: peteryefi@gmail.com
    """
    PARKING_GARAGE = "Parking Garage"
    POOL_AREA = "Pool Area"
    OPEN_OFFICE = "Open Office"
    HALL = "Hall"
    CORRIDOR = "Corridor"
    STAIR_AREA = "StairArea"
    DINNING_AREA = "DinningArea"
    OTHER = "Other"
