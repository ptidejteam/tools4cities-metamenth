from metamenth.enumerations.abstract_enum import AbstractEnum


class RelationshipName(AbstractEnum):
    CONTAINS = "Contains"
    USES = "Uses"
    FEEDS = "Feeds"
    PART_OF = "PartOf"
    CONNECTED_TO = "ConnectedTo"
    CONTROLS = "Controls"
    OPERATES_ON = "OperatesOn"
    MONITORS = "Monitors"
    LOCATED_IN = "LocatedIn"

