from __future__ import annotations
from brick import Brick

class TreeNode:

    def __init__(self, brick: Brick):
        self.brick = brick
        self.left = None
        self.right = None
        self.up = None
        self.down = None

        # direction from parent, debugging / display
        self.dir_from_parent = None

        # for easier debugging / display
        self.parent = None

        # for astar search
        self.cost = 0   # actual cost upto this node
        self.f_score = 0  # g + h cost

    def __lt__(self, other: TreeNode):
        return self.f_score < other.f_score

    def __str__(self):
        return '[parent(hash): {}, parent->{}, f_score: {}, actual_cost: {}'.format(hash(self.parent), self.dir_from_parent, self.f_score, self.cost)

