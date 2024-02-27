from enum import Enum


class AbstractEnum(Enum):

    @classmethod
    def get_enum_type(cls, value: str):
        try:
            return cls[value]
        except KeyError:
            return None
