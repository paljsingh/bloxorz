from enum import Enum

class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


    @classmethod
    def get_directions(cls, order):
        charmap = {
            'L': Direction.LEFT,
            'R': Direction.RIGHT,
            'D': Direction.DOWN,
            'U': Direction.UP
        }
        for char in order:
            yield charmap[char]

        return
