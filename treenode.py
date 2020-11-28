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

        # for a-star search
        self.f_cost = 0  # g + h cost

    def __lt__(self, other: TreeNode):
        """
        Compare one treenode to another by f_cost, used to build a min-heap.
        :param other: Tree Node
        :return: True if current node has lower f_cost than other, False otherwise.
        """
        return self.f_cost < other.f_cost

    def __str__(self):
        """
        String representation.
        :return: Formatted string of object attributes values.
        """
        dir_name = self.dir_from_parent.name.lower() if self.dir_from_parent else "none"
        parent_hash = hash(self.parent) if self.parent else "none"

        return '[hash(Node): {}, hash(Parent): {}, Parent->{:5s}, row: {}, col: {}]'.format(
            hash(self), parent_hash, dir_name, self.brick.pos.y + 1, self.brick.pos.x + 1)
