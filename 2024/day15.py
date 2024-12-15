#!/usr/bin/env python
'''
https://adventofcode.com/2024/day/15
'''
import itertools
import sys
import textwrap
from collections import defaultdict, namedtuple
from collections.abc import Sequence
from typing import Callable, Literal

# Local imports
from aoc import AOC, TupleMixin, XY, directions

tile = namedtuple(
    'MapTile',
    ('ROBOT', 'WALL', 'EMPTY', 'SMALL_BOX', 'BIG_BOX_LEFT', 'BIG_BOX_RIGHT')
)(
    '@', '#', '.', 'O', '[', ']',
)

UP = '^'
DOWN = 'v'
LEFT = '<'
RIGHT = '>'

# Type hints
Box = Literal[tile.SMALL_BOX, tile.BIG_BOX_LEFT, tile.BIG_BOX_RIGHT]
Tile = Literal[tile.ROBOT, tile.WALL, tile.EMPTY, Box]
Move = Literal[UP, DOWN, LEFT, RIGHT]
Moves = Sequence[Move]
Obstacles = dict[Box, set[XY]]


class Obstruction(Exception):
    '''
    Raised when moving would push up against a wall tile
    '''


class Warehouse(TupleMixin):
    '''
    Simulate the warehouse and track contents
    '''
    def __init__(
        self,
        data: str,
        moves: Moves,
        supersize: bool = False,
    ) -> None:
        '''
        Load the file from the Path object
        '''
        self.moves: Moves = moves

        row_index: int
        row: Sequence[Tile]
        col_index: int
        col: Tile

        robot: XY | None = None
        wall_init: set[XY] = set()
        small_box_init: set[XY] = set()
        big_box_left_init: set[XY] = set()
        big_box_right_init: set[XY] = set()

        if supersize:
            data = data.replace('#', '##').replace('O', '[]').replace('.', '..').replace('@', '@.')

        # Load the items from the input into sets of coordinate pairs
        for row_index, row in enumerate(data.splitlines()):
            for col_index, col in enumerate(row):
                coord: XY = (row_index, col_index)
                match col:
                    case tile.ROBOT:
                        robot = coord
                    case tile.WALL:
                        wall_init.add(coord)
                    case tile.SMALL_BOX:
                        small_box_init.add(coord)
                    case tile.BIG_BOX_LEFT:
                        big_box_left_init.add(coord)
                    case tile.BIG_BOX_RIGHT:
                        big_box_right_init.add(coord)

        if robot is None:
            raise ValueError('Robot location not identified')

        # Freeze the initial state to preserve it
        self.robot_init = robot
        self.wall: frozenset[XY] = frozenset(wall_init)
        self.small_box: frozenset[XY] = frozenset(small_box_init)
        self.big_box_left: frozenset[XY] = frozenset(big_box_left_init)
        self.big_box_right: frozenset[XY] = frozenset(big_box_right_init)

    def move_robot(self) -> None:
        '''
        Move the robot (and boxes) according to the list of moves. Return the
        sum of the GPS coordinates of the boxes.
        '''
        robot: XY = self.robot_init
        small_box: set[XY] = set(self.small_box)
        big_box_left: set[XY] = set(self.big_box_left)
        big_box_right: set[XY] = set(self.big_box_right)

        move_map: dict[str, XY] = {
            UP: directions.NORTH,
            DOWN: directions.SOUTH,
            LEFT: directions.WEST,
            RIGHT: directions.EAST,
        }

        def _find_obstacles(
            start: XY,
            heading: Move,
            obstacles: Obstacles | None = None
        ) -> Obstacles:
            '''
            Look in the specified direction until empty space is found. If a
            wall is encountered, raise an exception.
            '''
            obstacles: Obstacles = obstacles or defaultdict(set)
            ptr: XY = start

            while True:
                ptr = self.tuple_add(ptr, move_map[heading])

                if ptr in self.wall:
                    raise Obstruction

                if ptr in small_box:
                    obstacles[tile.SMALL_BOX].add(ptr)

                elif ptr in big_box_left:
                    obstacles[tile.BIG_BOX_LEFT].add(ptr)
                    if heading in (UP, DOWN):
                        other_half: XY = self.tuple_add(ptr, directions.EAST)
                        obstacles[tile.BIG_BOX_RIGHT].add(other_half)
                        obstacles.update(
                            _find_obstacles(other_half, heading, obstacles)
                        )

                elif ptr in big_box_right:
                    obstacles[tile.BIG_BOX_RIGHT].add(ptr)
                    if heading in (UP, DOWN):
                        other_half: XY = self.tuple_add(ptr, directions.WEST)
                        obstacles[tile.BIG_BOX_LEFT].add(other_half)
                        obstacles.update(
                            _find_obstacles(other_half, heading, obstacles)
                        )

                else:
                    # An empty space has been reached
                    return obstacles

        #self.print(
        #    robot=robot,
        #    small_box=small_box,
        #    big_box_left=big_box_left,
        #    big_box_right=big_box_right,
        #)

        move: Move
        for move in self.moves:

            if move == '\n':
                continue

            try:
                obstacles: Obstacles = _find_obstacles(robot, move)
            except Obstruction:
                continue

            # "Move" all of the boxes by first removing them from the set, and
            # then adding back copies that are offset in the direction the
            # robot is moving.
            delta: XY = move_map[move]
            advance: Callable[[XY], XY] = lambda xy, delta=delta: self.tuple_add(
                xy,
                delta
            )

            small_box -= obstacles[tile.SMALL_BOX]
            small_box.update(map(advance, obstacles[tile.SMALL_BOX]))

            big_box_left -= obstacles[tile.BIG_BOX_LEFT]
            big_box_left.update(map(advance, obstacles[tile.BIG_BOX_LEFT]))

            big_box_right -= obstacles[tile.BIG_BOX_RIGHT]
            big_box_right.update(map(advance, obstacles[tile.BIG_BOX_RIGHT]))

            # Move the robot, now that the obstacles have been moved
            robot = self.tuple_add(robot, move_map[move])

            #self.print(
            #    robot=robot,
            #    small_box=small_box,
            #    big_box_left=big_box_left,
            #    big_box_right=big_box_right,
            #)

        # GPS coordinates are based off the location of the small box, or for
        # supersized warehouses, the left side of a big box. Since we'll only
        # have one or the other, they can both be passed to
        # itertools.chain.from_iterable(), and what gets spit out will be a
        # sequence of row/col pairs, which can be fed into the generator
        # expression.
        return sum(
            (100 * row) + col
            for row, col in itertools.chain.from_iterable(
                (small_box, big_box_left)
            )
        )

    def print(
        self,
        robot: XY,
        small_box: set[XY],
        big_box_left: set[XY],
        big_box_right: set[XY],
    ) -> None:
        '''
        Print the current state of the warehouse map to stdout
        '''
        max_row: int
        max_col: int
        buckets: list[set[XY]] = [
            self.wall, small_box, big_box_left, big_box_right
        ]

        max_row, max_col = map(
            max,
            zip(*itertools.chain.from_iterable(buckets)),
        )
        for row_index in range(max_row + 1):
            for col_index in range(max_col + 1):
                coord: XY = (row_index, col_index)
                char: Tile
                if coord in self.wall:
                    char = tile.WALL
                elif coord in small_box:
                    char = tile.SMALL_BOX
                elif coord in big_box_left:
                    char = tile.BIG_BOX_LEFT
                elif coord in big_box_right:
                    char = tile.BIG_BOX_RIGHT
                elif coord == robot:
                    char = tile.ROBOT
                else:
                    char = tile.EMPTY
                sys.stdout.write(char)
            sys.stdout.write('\n')

        sys.stdout.write('\n')
        sys.stdout.flush()


class AOC2024Day15(AOC):
    '''
    Day 15 of Advent of Code 2024
    '''
    example_data_part1: str = textwrap.dedent(
        '''
        ########
        #..O.O.#
        ##@.O..#
        #...O..#
        #.#.O..#
        #...O..#
        #......#
        ########

        <^^>>>vv<v>>v<<
        '''
    )

    example_data_part2: str = textwrap.dedent(
        '''
        ##########
        #..O..O.O#
        #......O.#
        #.OO..O.O#
        #..O@..O.#
        #O#..O...#
        #O..O..O.#
        #.OO.O.OO#
        #....O...#
        ##########

        <vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
        vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
        ><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
        <<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
        ^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
        ^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
        >^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
        <><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
        ^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
        v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^
        '''
    )

    validate_part1: int = 2028
    validate_part2: int = 9021

    def part1(self) -> int:
        '''
        Return the sum of the GPS coordinates for each box after simulating the
        robot's movements.
        '''
        warehouse: Warehouse = Warehouse(*self.input_part1.strip().split('\n\n'))
        return warehouse.move_robot()

    def part2(self) -> int:
        '''
        Return the sum of the GPS coordinates for each box after simulating the
        robot's movements. In this example, additionally perform a translation
        on the map to "supersize" everything in it.
        '''
        warehouse: Warehouse = Warehouse(
            *self.input_part2.strip().split('\n\n'),
            supersize=True,
        )
        return warehouse.move_robot()


if __name__ == '__main__':
    aoc = AOC2024Day15()
    aoc.run()
