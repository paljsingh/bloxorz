from __future__ import annotations
from typing import Generator
from enum import Enum


class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

    @classmethod
    def get_directions(cls, order: str) -> Generator[Direction]:
        char_map = {
            'L': Direction.LEFT,
            'R': Direction.RIGHT,
            'D': Direction.DOWN,
            'U': Direction.UP
        }
        for char in order:
            yield char_map[char]

        return
