from __future__ import annotations
from typing import List
from enum import Enum


class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

    @classmethod
    def get_directions(cls, order: str) -> List[Direction]:
        """
        Return Direction enumerations in specified order.
        :param order: string containing a permutation of characters 'L', 'R', 'U', 'D'.
        :return: List of direction enumerations in specified order.
        """
        char_map = {
            'L': Direction.LEFT,
            'R': Direction.RIGHT,
            'D': Direction.DOWN,
            'U': Direction.UP
        }
        directions = list()
        for char in order:
            directions.append(char_map[char])

        return directions
