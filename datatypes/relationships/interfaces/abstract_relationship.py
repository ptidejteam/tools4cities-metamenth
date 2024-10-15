from abc import ABC
from enumerations import RelationshipName


class AbstractRelationship(ABC):
    def __init__(self, name: RelationshipName):
        self.name = name
