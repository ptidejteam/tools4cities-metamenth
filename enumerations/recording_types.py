from enum import Enum


class RecordingType(Enum):
    """
    Various sensor measurement types

    Author: Peter Yefi
    Email: peteryefi@gmail.com
    """
    BINARY = "Binary"
    LINEAR = "Linear"
    CONTINUOUS = "Continuous"
    EXPONENTIAL = "Exponential"
