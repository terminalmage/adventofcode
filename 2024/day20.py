#!/usr/bin/env python
'''
https://adventofcode.com/2024/day/20
'''
import itertools
import textwrap
from collections import deque
from typing import Literal

# Local imports
from aoc import AOC, Grid, XY

EMPTY: str = '.'
WALL: str = '#'

# Type hints
Tile = Literal[EMPTY, WALL]
CheatStart = XY
CheatEnd = XY
Cheat = tuple[CheatStart, CheatEnd]
MazePath = tuple[XY, ...]


class Maze(Grid):
    '''
    Represents the map
    '''
    def __init__(self, data: str):
        '''
        Load the input into the grid
        '''
        super().__init__(data)
        self.start = self.find('S')
        self.goal = self.find('E')

    def best_path(self) -> MazePath:
        '''
        BFS solution to return the best path, as a tuple of coordinate pairs
        from the start to the end, inclusive.
        '''
        dq: deque[tuple[XY, MazePath]] = deque([(self.start, (self.start,))])

        # Track coordinates we have visited. Due to how BFS works (always
        # trying the next closest coordinate in all directions), we know that
        # if a later loop iteration reaches a given coordinate, it will not be
        # the fastest to reach that coordinate, and cannot possibly be part of
        # the optimal path to the goal.
        visited: set[XY] = set()

        pos: XY
        path: XY
        while dq:
            pos, path = dq.popleft()

            if pos == self.goal:
                # This is the first attempt to reach the goal, and therefore
                # the one to reach the goal in the fewest steps. Return the
                # path taken.
                return path

            if pos in visited:
                # Don't double back on coordinates we've already visited, they
                # will be guaranteed not to be part of the optimal path.
                continue
            visited.add(pos)

            # Attempt movement in every direction, except when you would
            # tread on an already-visited coordinate, or run into a wall
            neighbor: XY
            tile: Tile
            for neighbor, tile in self.neighbors(pos):
                if neighbor not in visited and tile != WALL:
                    dq.append((neighbor, path + (neighbor,)))

    def good_cheats(self, max_cheat: int, improvement: int) -> list[Cheat]:
        '''
        Yields a sequence of shortcuts which satisfy both of the following
        criteria:

            1. Length in steps (calculated as Manhattan Distance) of the
               shortcut is <= max_cheat.
            2. The shortcut results in an improvement over the best path which
               is >= the specified threshold.

        To do this, first get the best path through the maze, and then use the
        coordinates in that path to build up a dictionary of the distances from
        the starting point. The starting point will have a distance of 0, the
        next step in the path has a distance of 1, etc. Next, do the same from
        the other direction (i.e. build a mapping of path coordinates to
        distances from the end).

        A shortcut must both start and end on the path, so the set of possible
        shortcuts can be represented as the unique combinations of 2 points on
        the path.

        Using the distance mappings, we can represent the new path length
        (taking into account the shortcut) by adding together the following:

            1. Shortcut length
            2. Length from start of path to start of shortcut
            3. Length from end of path to end of shortcut

        '''
        # Get the best path through the maze, represented as a tuple of
        # coordinate pairs of points along the path.
        path: MazePath = self.best_path()

        # Get distance mappings
        steps_from_start = {
            coord: index
            for index, coord in enumerate(path)
        }
        steps_from_end = {
            coord: index
            for index, coord in enumerate(reversed(path))
        }

        # List to aggregate shortcuts which fit the criteria
        ret: list[Cheat] = []

        cheat_start: CheatStart
        cheat_end: CheatEnd
        for cheat_start, cheat_end in itertools.combinations(path, 2):
            # distance() comes from the XYMixin (parent of Grid class), and
            # calculates the Manhattan Distance between the two points. This is
            # the number of steps in the shortcut.
            cheat_len: int = self.distance(cheat_start, cheat_end)
            if cheat_len > max_cheat:
                # Invalid cheat (too long)
                continue

            path_len_with_cheat = sum((
                cheat_len,
                steps_from_start[cheat_start],
                steps_from_end[cheat_end],
            ))
            if len(path) - path_len_with_cheat >= improvement:
                # This is only a "good" cheat if it saves more than the
                # specified threshold of steps.
                ret.append((cheat_start, cheat_end))

        return ret


class AOC2024Day20(AOC):
    '''
    Day 20 of Advent of Code 2024
    '''
    example_data: str = textwrap.dedent(
        '''
        ###############
        #...#...#.....#
        #.#.#.#.#.###.#
        #S#...#.#.#...#
        #######.#.#.###
        #######.#.#...#
        #######.#.###.#
        ###..E#...#...#
        ###.#######.###
        #...###...#...#
        #.#####.#.###.#
        #.#...#.#.#...#
        #.#.#.#.#.#.###
        #...#...#...###
        ###############
        '''
    )

    validate_part1: int = 5
    validate_part2: int = 285

    # Set by post_init
    maze = None

    def post_init(self) -> None:
        '''
        Load the input into a Maze object
        '''
        self.maze: Maze = Maze(self.input)

    def part1(self) -> int:
        '''
        Calculate the number of cheats of length <= 2 which save at least the
        specified amount of steps.
        '''
        improvement: int = 20 if self.example else 100
        return len(self.maze.good_cheats(max_cheat=2, improvement=improvement))

    def part2(self) -> str:
        '''
        Calculate the number of cheats of length <= 20 which save at least the
        specified amount of steps.
        '''
        improvement: int = 50 if self.example else 100
        return len(self.maze.good_cheats(max_cheat=20, improvement=improvement))


if __name__ == '__main__':
    aoc = AOC2024Day20()
    aoc.run()
