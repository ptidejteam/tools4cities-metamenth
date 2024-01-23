import uuid
from structure.cover import Cover
from typing import List


class Envelope:
    """
    The envelope of a building

    Author: Peter Yefi
    Email: peteryefi@gmail.com
    """
    def __init__(self):
        self.UID = str(uuid.uuid4())
        self.covers: List['Cover'] = []

    def add_cover(self, cover: Cover):
        """
        Adds a cover to a building
        :param cover: the building cover e.g., wall, roof
        :return:
        """
        self.covers.append(cover)

    def __str__(self):
        cover_details = "\n".join(str(cover) for cover in self.covers)
        return (
            f"Cover("
            f"UID: {self.UID}, "
            f"Layers:\n{cover_details})"
        )
