from abc import ABC
from enumerations import RelationshipType
class AbstractRelationship(ABC):
    def __init__(self, name, relationship_type):
        self.name = name
        self.relationship_type =