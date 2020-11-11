#!/usr/bin/env python3
from typing import List
from orientation import Orientation
from direction import Direction
from brick import Brick
from pos import Pos
from math import sqrt, inf
from treenode import TreeNode
import locale
import argparse

class Bloxorz:

    def __init__(self, world: List[List[int]], args: argparse.Namespace):
        self.world = world
        self.args = args
        self.dfs_steps = 0

    # does a brick with given position fall off the world map?
    def is_off_map(self, pos: Pos):

        for x,y in Brick(pos).get_positions_occupied():

            # bad coordinates, outside the matrix.
            if x < 0 or y < 0 or x >= len(self.world[0]) or y >= len(self.world):
                return True

            # no-tile positions
            if self.world[y][x] == 0:
                return True

        return False

    # Is a move feasible in the given direction?
    def is_valid_move(self, brick: Brick, direction: Direction) -> Pos:

        # find next position in the given direction
        next_pos = brick.next_pos(direction)

        # if the next position is off-map, return.
        if self.is_off_map(next_pos):
            return None

        return next_pos

    def solve_by_heuristic(self, brick: Brick):
        self.show(brick)
        for direction in [ Direction.DOWN, Direction.RIGHT, Direction.RIGHT, Direction.RIGHT, Direction.RIGHT, Direction.RIGHT, Direction.RIGHT, Direction.DOWN]:
            next_pos = self.is_valid_move(brick, direction)
            if next_pos:
                brick.move(next_pos)
            else:
                return

            print("\n{:>20s} {:5s}\n".format("====>", direction.name))
            self.show(brick)

    def is_goal_state(self, pos: Pos) -> bool:
        if pos.orientation is Orientation.STANDING and self.world[pos.y][pos.x] == 9:
            return True
        return False

    def distance_euclidian(self, pos1: Pos, pos2: Pos) -> float:
        return sqrt((pos1.x - pos2.x) ** 2 + (pos1.y - pos2.y) ** 2)

    def distance_manhattan(self, pos1: Pos, pos2: Pos) -> int:
        return abs(pos1.x - pos2.x) + abs(pos1.y - pos2.y)

    def get_tree_level(self, node: TreeNode) -> int:
        level = 0
        tmpnode = node
        while tmpnode.parent is not None:
            level += 1
            tmpnode = tmpnode.parent
        return level

    def show_tree_bfs(self, treehead: TreeNode):
        queue = list()
        queue.append(treehead)
        steps = 0
        while len(queue) > 0:
            node = queue.pop(0)
            print ("\nSteps: {}, Level: {}, Node(hash): {}, Parent(hash): {}, Parent->{}".format(
                steps, self.get_tree_level(node), node.__hash__(), node.parent.__hash__(), node.dir_from_parent))
            self.show(node.brick)

            steps += 1
            if self.is_goal_state(node.brick.pos):
                print("\n{:>80s}".format("FOUND GOAL STATE !!!!"))
                print("{:>80s}".format("BFS SEARCH CAN STOP HERE!\n"))
                return

            for direction in [Direction.LEFT, Direction.RIGHT, Direction.UP, Direction.DOWN]:
                next_node = getattr(node, direction.name.lower())
                if next_node is not None:
                    queue.append(next_node)

    # make state tree given the current brick position on the world map.
    def make_state_tree_bfs(self, head: TreeNode):
        visited_pos = list()
        visited_pos.append(head.brick.pos)
        node_queue = list()
        node_queue.append(head)

        while len(node_queue) > 0:
            node = node_queue.pop(0)
            for direction in [Direction.LEFT, Direction.RIGHT, Direction.UP, Direction.DOWN]:
                next_pos = self.is_valid_move(node.brick, direction)
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

    def solve_by_bfs(self, brick: Brick):
        treehead = TreeNode(brick)
        self.make_state_tree_bfs(treehead)
        self.show_tree_bfs(treehead)

    def show_tree_dfs(self, node: TreeNode, visited_pos=None):
        if visited_pos is None:
            visited_pos = list()

        visited_pos.append(node.brick.pos)
        print ("\nSteps: {}, Level: {}, Node(hash): {}, Parent(hash): {}, Parent->{}".format(
            self.dfs_steps, self.get_tree_level(node), node.__hash__(), node.parent.__hash__(), node.dir_from_parent))
        self.show(node.brick)
        self.dfs_steps += 1
        if self.is_goal_state(node.brick.pos):
            print("\n{:>80s}".format("FOUND GOAL STATE !!!!"))
            print("{:>80s}".format("DFS SEARCH CAN STOP HERE!\n"))
            return

        for direction in [Direction.LEFT, Direction.RIGHT, Direction.UP, Direction.DOWN]:
            next_node = getattr(node, direction.name.lower())
            if next_node and next_node.brick.pos not in visited_pos:
                self.show_tree_dfs(next_node, visited_pos)

    # make state tree given the current brick position on the world map.
    def make_state_tree_dfs(self, node: TreeNode, visited_pos=None):
        if visited_pos is None:
            visited_pos = list()
            visited_pos.append(node.brick.pos)

        for direction in [Direction.LEFT, Direction.RIGHT, Direction.UP, Direction.DOWN]:
            next_pos = self.is_valid_move(node.brick, direction)
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

                self.make_state_tree_dfs(new_node, visited_pos)
        return

    def solve_by_dfs(self, brick: Brick):
        treehead = TreeNode(brick)
        self.make_state_tree_dfs(treehead)
        self.show_tree_dfs(treehead)

    def astar_heuristic_cost(self, target_pos: Pos):
        costs = dict()
        num = 0
        for y in range(len(self.world)):
            for x in range(len(self.world[0])):
                pos = Pos(x, y)
                if not self.is_off_map(pos):
                    costs[num] = self.distance_euclidian(pos, target_pos)
                else:
                    costs[num] = inf
                num += 1
        return costs

    # minimum g+h cost from current brick position to next feasible brick position.
    def min_g_h_cost(self, node: TreeNode, h_costs, visited_pos):
        min_cost = inf
        min_cost_move = None

        for direction in [Direction.LEFT, Direction.RIGHT, Direction.UP, Direction.DOWN]:
            next_pos = self.is_valid_move(node.brick, direction)
            if next_pos and next_pos not in visited_pos:    # valid move
                g_cost = node.cost + 1  # cost to reach next node is current cost + 1
                index = next_pos.y * len(self.world[0]) + next_pos.x
                if g_cost + h_costs[index] < min_cost:
                    min_cost = g_cost + h_costs[index]
                    min_cost_move = next_pos
                    min_cost_dir = direction

        return (min_cost_move, g_cost, min_cost_dir)

    def solve_by_astar(self, brick: Brick, target_pos: Pos):
        # compute the heuristic cost from all valid positions to the target positions
        heuristic_costs = self.astar_heuristic_cost(target_pos)

        visited_pos = list()

        steps = 0
        head = TreeNode(brick)
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
            print("\nSteps: {}, Parent->{}".format(steps, new_node.dir_from_parent))
            self.show(new_node.brick)

            visited_pos.append(next_pos)
            node = new_node


    def show(self, brick: Brick):
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
                if [x, y] in brick.get_positions_occupied():
                    print(style['occupied'], end="")
                elif self.world[y][x] == 9:
                    print(style['target'], end="")
                else:
                    tile_char = style['tile'] if self.world[y][x] == 1 else style['notile']
                    print(tile_char, end="")

            print("")


parser = argparse.ArgumentParser(description='Bloxorz python implementation.')
parser.add_argument('--search', '-s', choices=['bfs', 'dfs', 'astar'], default='astar', help='search method.')
parser.add_argument('--style', '-t', choices=['ascii', 'utf8'], default='utf8', help='world map display style.')

args = parser.parse_args()

def get_target_position(matrix: List[List[int]]):
    for y in range(len(matrix)):
        for x in range(len(matrix[0])):
            if matrix[y][x] == 9:
                return (x, y)

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

    if args.search == 'bfs':
        blox.solve_by_bfs(brick)
    elif args.search == 'dfs':
        blox.solve_by_dfs(brick)
    else:
        x, y = get_target_position(matrix)
        blox.solve_by_astar(brick, Pos(x, y, Orientation.STANDING))