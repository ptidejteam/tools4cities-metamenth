from enumerations import BuildingEntity


class EntityInsert:
    """
    A visitor that remove entities from objects
    """

    def __init__(self):
        pass

    @staticmethod
    def insert_space_entity(space, entity, entity_type):
        """
        Adds am entity to a space
        :param space: the space entity (room or open space) of type AbstractFloorEntity
        :param entity: the entity (e.g. transducer, appliance, equipment, etc)
        :param entity_type: the type of entity
        :return:
        """

        if entity_type == BuildingEntity.TRANSDUCER.value:
            # add tranducer to open space or room
            existing_transducer = next(
                (transducer for transducer in space.transducers if transducer.name == entity.name),
                None
            )

            if existing_transducer is None:
                space.transducers.append(entity)

