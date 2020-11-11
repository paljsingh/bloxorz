#!/usr/bin/env python3
from typing import List, Dict, Tuple
from orientation import Orientation
from direction import Direction
from brick import Brick
from pos import Pos
from math import sqrt, inf
from treenode import TreeNode
import argparse

class Bloxorz:
    """
    Bloxorz
    The application runs the first round of Bloxorz game.
    The search is implemented using BFS, DFS and A* algorithms.
    For A* it uses heuristic scores based on Euclidean distance to the target.
    """

    def __init__(self, world: List[List[int]], args: argparse.Namespace):
        """
        Initialize the params required for BFS/DFS/A* searches.
        :param world: The world map, m*n matrix.
            Matrix elements with value 0 are considered unavailable tiles / holes.
            Elements with value 1 are the regular tiles available for brick navigation.
            Target tile is expected to have value 9.
        :param args: Extra arguments specifying the search algorithm to use, and display style.
        """
        self.world = world
        self.args = args

        # class level variables for dfs search.
        self.dfs_steps = 0
        self.dfs_target_found = False

    def is_off_map(self, pos: Pos) -> bool:
        """
        Checks if the given position (x, y coordinates + brick orientation) leads the
        brick to fall off the world map.
        :param pos: Position object containing x, y coordinates and brick orientation.
        :return: True, if the brick will fall off the map, False otherwise.
        """

        for x,y in Brick(pos).get_blocks_occupied():

            # bad coordinates, outside the matrix.
            if x < 0 or y < 0 or x >= len(self.world[0]) or y >= len(self.world):
                return True

            # no-tile positions
            if self.world[y][x] == 0:
                return True

        return False

    def valid_move(self, brick: Brick, direction: Direction) -> Pos:
        """
        If the brick move in given direction is valid, return the new position object,
        returns None otherwise.
        :param brick: Brick object.
        :param direction: direction (left, right, up or down)
        :return: New position object or None if the move is not feasible.
        """

        # find next position in the given direction
        next_pos = brick.next_pos(direction)

        # if the next position is off-map, return.
        if self.is_off_map(next_pos):
            return None

        return next_pos

    def is_target_state(self, pos: Pos) -> bool:
        """
        Check if the given position is the target state.
        :param pos: Position object.
        :return: True if the position/orientation matches the target state, False otherwise.
        """
        if pos.orientation is Orientation.STANDING and self.world[pos.y][pos.x] == 9:
            return True
        return False

    def get_node_depth(self, node: TreeNode) -> int:
        """
        Compute the depth of a given tree node.
        :param node: Tree node.
        :return: Depth value as distance of the node from the root node.
        """
        level = 0
        tmpnode = node
        while tmpnode.parent is not None:
            level += 1
            tmpnode = tmpnode.parent
        return level

    """
    BFS SPECIFIC FUNCTIONS
    """

    def solve_by_bfs(self, head: TreeNode):
        """
        Search the state space using BFS search.
        :param head: Tree head node.
        """

        # visited list to store visited position on the world map.
        visited_pos = list()
        visited_pos.append(head.brick.pos)

        # queue to hold nodes encountered at each level of the tree.
        node_queue = list()
        node_queue.append(head)

        steps = 0
        while len(node_queue) > 0:
            node = node_queue.pop(0)

            # show the BFS tree.
            print ("\nSteps: {}, Level: {}, Node(hash): {}, Parent(hash): {}, Parent->{}".format(
                steps, self.get_node_depth(node), node.__hash__(), node.parent.__hash__(), node.dir_from_parent))
            self.show(node.brick)

            steps += 1
            if self.is_target_state(node.brick.pos):
                return

            for direction in [Direction.LEFT, Direction.RIGHT, Direction.UP, Direction.DOWN]:
                next_pos = self.valid_move(node.brick, direction)
                if next_pos and next_pos not in visited_pos:
                    # create a new brick with next_pos, initialize a new node with brick position
                    # and recursively make the state tree.
                    new_brick = Brick(next_pos)
                    new_node = TreeNode(new_brick)

                    # set the 4 direction attributes
                    setattr(node, direction.name.lower(), new_node)

                    # and parent node of the new node.
                    new_node.parent = node
                    new_node.dir_from_parent = direction.name.lower()


                    node_queue.append(new_node)
                    visited_pos.append(next_pos)

        return


    """
    DFS SPECIFIC FUNCTIONS. 
    """

    # make state tree given the current brick position on the world map.
    def _dfs_search_tree(self, node: TreeNode, visited_pos: List =None):
        """
        Search the state space using DFS algorithm.
        :param node: Tree node.
        :param visited_pos: List containing visited positions.
        """
        if self.dfs_target_found:
            return

        if visited_pos is None:
            visited_pos = list()
            visited_pos.append(node.brick.pos)

        print ("\nSteps: {}, Level: {}, Node(hash): {}, Parent(hash): {}, Parent->{}".format(
            self.dfs_steps, self.get_node_depth(node), node.__hash__(), node.parent.__hash__(), node.dir_from_parent))
        self.show(node.brick)
        self.dfs_steps += 1     # class level variable.

        if self.is_target_state(node.brick.pos):
            self.dfs_target_found = True
            return

        for direction in [Direction.LEFT, Direction.RIGHT, Direction.UP, Direction.DOWN]:
            next_pos = self.valid_move(node.brick, direction)
            if next_pos and next_pos not in visited_pos:
                # create a new brick with next_pos, initialize a new node with brick position
                # and recursively make the state tree.
                new_brick = Brick(next_pos)
                new_node = TreeNode(new_brick)

                # set the 4 direction attributes
                setattr(node, direction.name.lower(), new_node)

                # and parent node of the new node.
                new_node.parent = node
                new_node.dir_from_parent = direction.name.lower()
                visited_pos.append(next_pos)

                self._dfs_search_tree(new_node, visited_pos)
        return

    def solve_by_dfs(self, head: TreeNode):
        """
        Wrapper function to initiate DFS search.
        :param brick: Brick object.
        """
        self._dfs_search_tree(head)


    """
    A* SEARCH SPECIFIC FUNCTIONS
    """
    def distance_euclidean(self, pos1: Pos, pos2: Pos) -> float:
        """
        Compute euclidean distance between two given block positions.
        :param pos1: First Position object.
        :param pos2: Second Position object.
        :return: Euclidean distance between the two coordinates.
        """
        return sqrt((pos1.x - pos2.x) ** 2 + (pos1.y - pos2.y) ** 2)

    def distance_manhattan(self, pos1: Pos, pos2: Pos) -> int:
        """
        Compute manhattan distance between two given block positions.
        :param pos1: First Position object.
        :param pos2: Second Position object.
        :return: Manhattan distance between the two coordinates.
        """
        return abs(pos1.x - pos2.x) + abs(pos1.y - pos2.y)

    def astar_heuristic_cost(self, target_pos: Pos) -> Dict:
        """
        Compute heuristic costs for each block on the world map to the target block.
        :param target_pos: Target block position.
        :return:
        """
        costs = dict()
        num = 0
        for y in range(len(self.world)):
            for x in range(len(self.world[0])):
                pos = Pos(x, y)
                if not self.is_off_map(pos):
                    costs[num] = self.distance_euclidean(pos, target_pos)
                else:
                    costs[num] = inf
                num += 1
        return costs

    # minimum g+h cost from current brick position to next feasible brick position.
    def min_g_h_cost(self, node: TreeNode, h_costs: dict, visited_pos: list) -> Tuple:
        """
        Compute g_cost + h_cost for all the neighbors of a given node, and return the minimum cost.
        :param node: Current node.
        :param h_costs: Dictionary containing heuristic costs for all the blocks.
        :param visited_pos: List containing visited positions.
        :return: A tuple containing next_position corresponding to the minimum cost,
         along with its g_cost and associated direction (left, right, up, down).
        """
        min_cost = inf
        min_cost_pos = None
        min_cost_dir = None
        g_cost = node.cost + 1  # cost to reach all next node is current_cost + 1

        for direction in [Direction.LEFT, Direction.RIGHT, Direction.UP, Direction.DOWN]:
            next_pos = self.valid_move(node.brick, direction)
            if next_pos and next_pos not in visited_pos:    # valid move
                index = next_pos.y * len(self.world[0]) + next_pos.x
                if g_cost + h_costs[index] < min_cost:
                    min_cost = g_cost + h_costs[index]
                    min_cost_pos = next_pos
                    min_cost_dir = direction

        return (min_cost_pos, g_cost, min_cost_dir)

    def solve_by_astar(self, head: TreeNode, target_pos: Pos):
        """
        Solve the Bloxorz problem using A* algorithm.
        :param head: head node.
        :param target_pos: target position for heuristic estimates.
        """
        # compute the heuristic cost from all valid positions to the target positions
        heuristic_costs = self.astar_heuristic_cost(target_pos)

        visited_pos = list()

        steps = 0
        node = head

        print("\nSteps: {}, Parent->{}".format(steps, node.dir_from_parent))
        self.show(head.brick)

        while not node.brick.pos == target_pos:

            next_pos, min_cost, min_cost_dir = self.min_g_h_cost(node, heuristic_costs, visited_pos)
            new_node = TreeNode(Brick(next_pos))
            new_node.cost = min_cost
            new_node.dir_from_parent = min_cost_dir

            setattr(node, min_cost_dir.name.lower(), new_node)

            steps += 1
            print("\nSteps: {}, Parent->{}".format(steps, new_node.dir_from_parent.name.lower()))
            self.show(new_node.brick)

            visited_pos.append(next_pos)
            node = new_node

        return


    """
    UTILITY FUNCTIONS
    """

    def show(self, brick: Brick):
        """
        Display the world map and brick position.
        Defaults style is displaying the world map using unicode characters,
        this may not work on old terminal emulators lacking utf-8 support.
        Specify program arguments to use --style=ascii on such terminals.
        :param brick: Brick object.
        """
        if self.args.style == "utf8":
            style = dict({
                "tile": "⬜",
                "notile": "⬛",
                "occupied": "🟧",
                "target": "❎"
            })
        else:
            style = dict({
                "tile": "1",
                "notile": "0",
                "occupied": "X",
                "target": "+"
            })

        for y in range(len(self.world)):
            for x in range(len(self.world[0])):
                if [x, y] in brick.get_blocks_occupied():
                    print(style['occupied'], end="")
                elif self.world[y][x] == 9:
                    print(style['target'], end="")
                else:
                    tile_char = style['tile'] if self.world[y][x] == 1 else style['notile']
                    print(tile_char, end="")

            print("")


def get_target_position(matrix: List[List[int]]) -> Tuple:
    """
    Utility function to find the target block.
    :param matrix: m*n matrix.
    :return: A tuple containing x,y coordinates of the target block.
    """
    for y in range(len(matrix)):
        for x in range(len(matrix[0])):
            if matrix[y][x] == 9:
                return (x, y)

parser = argparse.ArgumentParser(description='Bloxorz python implementation.')
parser.add_argument('--search', '-s', choices=['bfs', 'dfs', 'astar'], default='astar', help='search method.')
parser.add_argument('--style', '-t', choices=['ascii', 'utf8'], default='utf8', help='world map display style.')

args = parser.parse_args()


if __name__ == '__main__':
    matrix = [
        [1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 1, 1, 9, 1, 1],
        [0, 0, 0, 0, 0, 0, 1, 1, 1, 0]
    ]

    blox = Bloxorz(matrix, args)

    (start_x, start_y) = (2, 2)

    # initialize the brick to start x,y (0 based index) and standing orientation.
    start_pos = Pos(start_x-1, start_y-1, Orientation.STANDING)
    brick = Brick(start_pos)
    head = TreeNode(brick)

    if args.search == 'bfs':
        blox.solve_by_bfs(head)
    elif args.search == 'dfs':
        blox.solve_by_dfs(head)
    else:
        x, y = get_target_position(matrix)
        blox.solve_by_astar(head, Pos(x, y, Orientation.STANDING))