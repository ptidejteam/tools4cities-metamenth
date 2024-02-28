from enum import Enum
from fuzzywuzzy import fuzz


class AbstractEnum(Enum):

    @classmethod
    def get_enum_type(cls, value: str):
        try:
            value = value.replace(" ", "_").replace("-", "_").upper()
            closest_key = max(cls.__members__.keys(), key=lambda k: fuzz.ratio(value.lower(), k.lower()))
            return cls[closest_key]
        except KeyError:
            return None
