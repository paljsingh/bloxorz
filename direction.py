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
