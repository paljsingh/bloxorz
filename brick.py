from direction import Direction
from orientation import Orientation
from pos import Pos


class Brick:

    def __init__(self, pos: Pos):
        self.pos = pos

    # return next position for given direction without any verification
    def next_pos(self, direction: Direction)-> Pos:

        # nextpos based on current position params.
        nextpos = Pos(self.pos.x, self.pos.y, self.pos.orientation)

        # update nextpos params based on current orientation and the direction of next move.
        # x value always points to the left block for horizontal lying brick
        # y values always points to the upper block for vertical lying brick
        if self.pos.orientation is Orientation.STANDING:
            if direction is Direction.UP:
                nextpos.y -= 2
                nextpos.orientation = Orientation.VERTICAL_LYING
            if direction is Direction.DOWN:
                nextpos.y += 1
                nextpos.orientation = Orientation.VERTICAL_LYING
            if direction is Direction.LEFT:
                nextpos.x -= 2
                nextpos.orientation = Orientation.HORIZONTAL_LYING
            if direction is Direction.RIGHT:
                nextpos.x += 1
                nextpos.orientation = Orientation.HORIZONTAL_LYING

        elif self.pos.orientation is Orientation.HORIZONTAL_LYING:
            if direction is Direction.UP:
                nextpos.y -= 1
            if direction is Direction.DOWN:
                nextpos.y += 1
            if direction is Direction.LEFT:
                nextpos.x -= 1
                nextpos.orientation = Orientation.STANDING
            if direction is Direction.RIGHT:
                nextpos.x += 2
                nextpos.orientation = Orientation.STANDING

        elif self.pos.orientation is Orientation.VERTICAL_LYING:
            if direction is Direction.UP:
                nextpos.y -= 1
                nextpos.orientation = Orientation.STANDING
            if direction is Direction.DOWN:
                nextpos.y += 2
                nextpos.orientation = Orientation.STANDING
            if direction is Direction.LEFT:
                nextpos.x -= 1
            if direction is Direction.RIGHT:
                nextpos.x += 1

        return nextpos


    # move to next given position.
    def move(self, next_pos: Pos):
        self.pos = next_pos

    def get_positions_occupied(self):

        # occupies 1 block in standing position
        if self.pos.orientation is Orientation.STANDING:
            return [[self.pos.x, self.pos.y]]

        # occupies 2 blocks along y axis in vertical pos.
        if self.pos.orientation is Orientation.VERTICAL_LYING:
            return [[self.pos.x, self.pos.y], [self.pos.x, self.pos.y + 1]]

        # occupies 2 blocks along x axis in horizontal pos.
        if self.pos.orientation is Orientation.HORIZONTAL_LYING:
            return [[self.pos.x, self.pos.y], [self.pos.x + 1, self.pos.y]]
