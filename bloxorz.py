#!/usr/bin/env python3

from typing import List, Dict, Tuple, Union
from orientation import Orientation
from direction import Direction
from brick import Brick
from pos import Pos
from math import sqrt, inf
from treenode import TreeNode
import argparse
from heapq import heappush, heappop
from collections import defaultdict

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

        # class level variable for A* search
        self.cost_visited = dict()

        self.show_args()


    def is_off_map(self, pos: Pos) -> bool:
        """
        Checks if the given position (x, y coordinates + brick orientation) leads the
        brick to fall off the world map.
        :param pos: Position object containing x, y coordinates and brick orientation.
        :return: True, if the brick will fall off the map, False otherwise.
        """

        for x, y in Brick(pos).get_blocks_occupied():

            # bad coordinates, outside the matrix.
            if x < 0 or y < 0 or x >= len(self.world[0]) or y >= len(self.world):
                return True

            # no-tile positions
            if self.world[y][x] == 0:
                return True

        return False

    def valid_move(self, brick: Brick, direction: Direction) -> Union[Pos, None]:
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
            print("Step: {}, Depth: {}, hash(Node): {}, hash(Parent): {}, Parent->{}".format(
                steps, self.get_node_depth(node), hash(node), hash(node.parent), node.dir_from_parent))
            self.show(node.brick)

            steps += 1
            if self.is_target_state(node.brick.pos):
                return

            for next_pos, direction in self.next_valid_move(node, visited_pos):
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
    def _dfs_search_tree(self, node: TreeNode, visited_pos: List = None):
        """
        Search the state space using DFS algorithm.
        :param node: Tree node.
        :param visited_pos: List containing visited positions.
        """

        if visited_pos is None:
            visited_pos = list()
            visited_pos.append(node.brick.pos)

        print("Step: {}, Depth: {}, hash(Node): {}, hash(Parent): {}, Parent->{}".format(
            self.dfs_steps, self.get_node_depth(node), hash(node), hash(node.parent), node.dir_from_parent))
        self.show(node.brick)
        self.dfs_steps += 1     # class level variable.

        if self.is_target_state(node.brick.pos):
            # with dfs, we are in deep recursion, 'return' won't exit the entire stack.
            exit(0)

        for next_pos, direction in self.next_valid_move(node, visited_pos):

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
        :param head: Tree node.
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
        :return: dictionary containing heuristics cost.
        """
        costs = dict()
        num = 0
        for y in range(len(self.world)):
            for x in range(len(self.world[0])):
                pos = Pos(x, y)
                if not self.is_off_map(pos):
                    if self.args.cost_method == 'euclidean':
                        costs[num] = self.distance_euclidean(pos, target_pos)
                    else:
                        costs[num] = self.distance_manhattan(pos, target_pos)
                else:
                    costs[num] = inf
                num += 1
        return costs

    def h_cost(self, h_costs: dict, node: TreeNode):
        pos = node.brick.pos

        if pos.orientation is Orientation.STANDING:
            return h_costs[pos.y * len(self.world[0]) + pos.x]

        if pos.orientation is Orientation.VERTICAL_LYING:
            return min(h_costs[pos.y * len(self.world[0]) + pos.x], h_costs[(pos.y + 1) * len(self.world[0]) + pos.x])

        if pos.orientation is Orientation.HORIZONTAL_LYING:
            return min(h_costs[pos.y * len(self.world[0]) + pos.x], h_costs[pos.y * len(self.world[0]) + (pos.x + 1)])

    def solve_by_astar(self, head: TreeNode, target_pos: Pos):
        """
        Solve the Bloxorz problem using A* algorithm.
        :param head: head node.
        :param target_pos: target position for heuristic estimates.
        """

        # compute the heuristic cost from all valid positions to the target positions
        heuristic_costs = self.astar_heuristic_cost(target_pos)
        head.f_cost = self.h_cost(heuristic_costs, head)
        self.cost_visited[self.get_index(head.brick.pos)] = 0

        expanded_nodes = list()

        steps = 0
        node = head

        print("Step: {}, Depth: {}, Cost: {}, hash(Node): {}, f_cost (current): {:.2f}".format(
                steps, self.get_node_depth(head), self.get_cost_visited(head.brick.pos), hash(head),self.h_cost(heuristic_costs, node)))
        self.show(head.brick)

        while True:
            # expand nodes
            for next_pos, direction in self.next_valid_move(node, []):
                if self.get_index(next_pos) not in self.cost_visited \
                        or self.get_cost_visited(node.brick.pos) + 1 < self.get_cost_visited(next_pos):

                    new_node = TreeNode(Brick(next_pos))
                    g_cost = self.get_cost_visited(node.brick.pos) + 1
                    h_cost = self.h_cost(heuristic_costs, new_node)
                    new_node.f_cost = g_cost + h_cost
                    self.debug("pushed - [hash(Node): {}, hash(Parent): {}, Parent->{:5s}, f_cost: {} + {:.2f} = {:.2f}] ".format(
                        hash(new_node), hash(node), direction.name.lower(), g_cost, h_cost, new_node.f_cost))
                    # set current node's child pointer.
                    setattr(node, direction.name.lower(), new_node)     # node.{left|right|up|down} -> new_node

                    # link new_node to the current node.
                    new_node.parent = node
                    new_node.dir_from_parent = direction
                    heappush(expanded_nodes, new_node)

            node = heappop(expanded_nodes)
            self.debug("popped - [hash(Node): {}, hash(Parent): {}, Parent->{:5s}, f_cost: {:.2f}]".format(
                hash(node), hash(node.parent), node.dir_from_parent.name.lower(), node.f_cost))

            # update cost of this node
            self.cost_visited[self.get_index(node.brick.pos)] = self.get_cost_visited(node.parent.brick.pos) + 1

            steps += 1
            print("Step: {}, Depth: {}, Cost: {}, hash(Node): {}, hash(Parent): {}, Parent->{}, f_cost: {:.2f}".format(
                steps, self.get_node_depth(node), self.get_cost_visited(node.brick.pos), hash(node),
                hash(node.parent), node.dir_from_parent.name.lower(), node.f_cost))
            self.show(node.brick)

            # exit conditions
            if node.brick.pos == target_pos:
                break

        print("\nA* SEARCH COMPLETED !")
        print("Optimal path is as below -> \n")
        self.show_optimal_path(node)
        return

    """
    UTILITY FUNCTIONS
    """

    def debug(self, message: str):
        if self.args.verbose:
            print(message)

    def get_index(self, pos: Pos) -> int:
        return pos.y * len(self.world[0]) + pos.x

    def get_cost_visited(self, pos: Pos):
        """
        cost from the visited nodes list.
        :param node:
        :return:
        """
        index = self.get_index(pos)
        return self.cost_visited[index]

    def next_valid_move(self, node: TreeNode, visited_pos: List):
        """
        get next valid move.
        :param node:
        :return:
        """
        for direction in Direction.get_directions(self.args.order):
            next_pos = self.valid_move(node.brick, direction)
            if next_pos and next_pos not in visited_pos:
                yield next_pos, direction
            else:
                self.debug("invalid/visited - [hash(Parent): {}, Parent->{:5s}]".format(hash(node), direction.name.lower()))
                continue

    def show_optimal_path(self, node: TreeNode):
        """
        Given a leaf node, traverse up to the root node, and display the path leading up to the leaf node.
        :param node: Leaf node.
        """
        node_stack = list()
        while node is not None:
            node_stack.append(node)
            node = node.parent

        # pop and print the list items
        while len(node_stack) > 0:
            node = node_stack.pop()
            if node.dir_from_parent is None:
                print("[START] ", end="")
            else:
                print("-> {} ".format(node.dir_from_parent.name.lower()), end="")
        print("[GOAL]\n\n")


    def show(self, brick: Brick):
        """
        Display the world map and brick position.
        Defaults style is displaying the world map using unicode characters,
        this may not work on old terminal emulators lacking utf-8 support.
        Specify program arguments to use --style=ascii on such terminals.
        :param brick: Brick object.
        """
        if self.args.style == "unicode":
            style = dict({
                "tile": "⬜",
                "hole": "⬛",
                "brick": "🟧",
                "target": "❎"
            })
        else:
            style = dict({
                "tile": "1",
                "hole": "0",
                "brick": "X",
                "target": "+"
            })

        for y in range(len(self.world)):
            for x in range(len(self.world[0])):
                if [x, y] in brick.get_blocks_occupied():
                    print(style['brick'], end="")
                elif self.world[y][x] == 9:
                    print(style['target'], end="")
                else:
                    tile_char = style['tile'] if self.world[y][x] == 1 else style['hole']
                    print(tile_char, end="")

            print("")
        print("")

    def show_args(self):
        self.debug("cost-method: {}".format(self.args.cost_method))
        self.debug("order: {}".format(self.args.order))
        self.debug("search: {}".format(self.args.search))
        self.debug("style: {}".format(self.args.style))
        self.debug("verbose: {}\n".format(self.args.verbose))


def get_target_position(matrix: List[List[int]]) -> Tuple:
    """
    Utility function to find the target block.
    :param matrix: m*n matrix.
    :return: A tuple containing x,y coordinates of the target block.
    """
    for y in range(len(matrix)):
        for x in range(len(matrix[0])):
            if matrix[y][x] == 9:
                return x, y


def validate_search_order(search_order):
    if len(search_order) == 4 and 'L' in search_order and 'R' in search_order \
            and 'U' in search_order and 'D' in search_order:
        return search_order

    raise argparse.ArgumentTypeError(
        "Bad search order '{}'. Must be a permutation of the characters 'L', 'R', 'U', 'D'".format(search_order))


epilog = """
Search order can be any permutation of the characters 'L', 'R', 'U', 'D'.
Some of the search algorithms (e.g. DFS) may work better with knowing the general direction of the target block. 
"""
parser = argparse.ArgumentParser(description='Bloxorz python implementation.', epilog=epilog, formatter_class=argparse.RawDescriptionHelpFormatter) # noqa
parser.add_argument('-c', '--cost-method', choices=['euclidean', 'manhattan'], default='euclidean', help='Distance metrics for heuristic cost for A*. (default=euclidean)')
parser.add_argument('-o', '--order', default='LRUD', type=validate_search_order, help='Order of search directions. (default=LRUD)')
parser.add_argument('-s', '--search', choices=['bfs', 'dfs', 'a-star'], default='a-star', help='Search method. (default=a-star)')
parser.add_argument('-t', '--style', choices=['ascii', 'unicode'], default='unicode', help='World map display style. (default=unicode)')
parser.add_argument('-v', '--verbose', action='store_true', help='verbose output.')

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

    # initialize the brick to (0 based index) x,y coordinates and a standing orientation.
    start_pos = Pos(start_x-1, start_y-1, Orientation.STANDING)
    brick = Brick(start_pos)
    head = TreeNode(brick)

    if args.search == 'bfs':
        blox.solve_by_bfs(head)
    elif args.search == 'dfs':
        blox.solve_by_dfs(head)
    elif args.search == 'a-star':
        x, y = get_target_position(matrix)
        blox.solve_by_astar(head, Pos(x, y, Orientation.STANDING))
    else:
        print("NO SUCH SEARCH ALGORITHM KNOWN '{}'".format(args.search))
