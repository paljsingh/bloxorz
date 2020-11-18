from __future__ import annotations
from orientation import Orientation


class Pos:

    def __init__(self, x: int, y: int, orientation: Orientation = Orientation.STANDING):
        self.x = x
        self.y = y
        self.orientation = orientation

    def __str__(self):
        """
        String representation of position object (for easier debugging)
        :return: Position object as string.
        """
        return '[x:{}, y:{}, orientation:{}]'.format(self.x, self.y, self.orientation)

    def __eq__(self, other: Pos) -> bool:
        """
        Compare current position object with another.
        :param other: The other position object.
        :return: True if the two objects match in x, y coordinates as well as their orientation.
        """
        return self.x == other.x and self.y == other.y and self.orientation == other.orientation
