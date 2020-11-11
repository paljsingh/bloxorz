from __future__ import annotations
from orientation import Orientation

class Pos:

    def __init__(self, x: int, y: int, orientation: Orientation = Orientation.STANDING):
        self.x = x
        self.y = y
        self.orientation = orientation

    def __str__(self):
        return 'x:{}, y:{}, orientation:{}'.format(self.x, self.y, self.orientation)

    # compare 2 nodes based on their brick positions for x,y,orientation
    def __eq__(self, other: Pos) -> bool:
        return self.x == other.x and self.y == other.y and self.orientation == other.orientation
