class AbstractSpaceVisitor:
    """
    Defines an interface for visiting
    spaces in buildings
    """
    def visit_building(self, building):
        pass

    def visit_zone(self, zone):
        pass

    def visit_floor(self, floor):
        pass

    def visit_room(self, room):
        pass

    def visit_open_space(self, open_space):
        pass
