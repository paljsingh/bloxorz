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
        self.cost = 0

