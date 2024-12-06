#!/usr/bin/env python
'''
https://adventofcode.com/2024/day/6
'''
import textwrap
from collections import deque
from collections.abc import Sequence
from pathlib import Path

# Local imports
from aoc import AOC, Grid, XY

# Type hints
Direction = XY
Position = XY
Visited = set[tuple[Position, Direction]]


class PatrolLoop(Exception):
    '''
    Raised when the guard hits a loop and fails to exit the map
    '''


class PatrolMap(Grid):
    '''
    Simulate the patrol map and track movements
    '''
    BLOCKED: str = '#'
    GUARD: str = '^'

    def __init__(
        self,
        data: Path | str | Sequence[str],
    ) -> None:
        '''
        Load the file from the Path object
        '''
        super().__init__(data)
        self.guard_init: XY = self.find(self.GUARD)

    @property
    def unique_positions(self) -> set[XY]:
        '''
        Return the number of unique positions the guard will visit while
        walking the map.
        '''
        return set(x[0] for x in self.walk_until_exit())

    def walk_until_exit(self):
        '''
        Walk the map, following the movement rules, until the guard exits. When
        the guard exits, return a set of all the positions and directions that
        the guard visited.
        '''
        guard: XY = self.guard_init
        directions: deque[XY] = deque(self.directions)
        visited: Visited = set([(guard, directions[0])])

        while True:
            new_pos: XY = self.tuple_add(guard, directions[0])
            if new_pos not in self:
                # Guard has exited the grid
                return visited
            if self[new_pos] == self.BLOCKED:
                # The tile ahead of the guard is blocked. Turn 90 degrees. This
                # is done by rotating the deque of directional deltas, which
                # happen to already be in clockwise order.
                directions.rotate(-1)
                # Don't update position yet (because we turned)
                continue

            # If we reached here, the tile ahead of the guard is empty
            key: Visited = (new_pos, directions[0])
            if key in visited:
                # The guard is in an endless loop and will never exit the map
                raise PatrolLoop

            visited.add(key)
            guard = new_pos


class AOC2024Day6(AOC):
    '''
    Day 6 of Advent of Code 2024
    '''
    example_data: str = textwrap.dedent(
        '''
        ....#.....
        .........#
        ..........
        ..#.......
        .......#..
        ..........
        .#..^.....
        ........#.
        #.........
        ......#...
        '''
    )

    validate_part1: int = 41
    validate_part2: int = 6

    # Set by post_init
    patrol_map = None

    def post_init(self) -> None:
        '''
        Load the input data
        '''
        self.patrol_map: PatrolMap = PatrolMap(self.input)

    def part1(self) -> int:
        '''
        Return the number of tiles visited. This is calculated by counting the
        number of unique positions the guard visits while walking the map.
        '''
        return len(self.patrol_map.unique_positions)

    def part2(self) -> int:
        '''
        Return the number of distinct obstacles that can be placed on the map
        to cause the guard to enter an endless loop.
        '''
        obstacles: set[XY] = set()

        pos: XY
        # Iterate over only the positions the guard would have walked, it's
        # pointless to add an obstacle in a place the guard would never visit.
        for pos in self.patrol_map.unique_positions:
            if pos == self.patrol_map.guard_init:
                # Skip, we can't add an obstacle in the same place where the
                # guard is standing
                continue
            orig_val: str = self.patrol_map[pos]
            if orig_val == self.patrol_map.BLOCKED:
                # If there was already an obstacle here, we can't add one
                continue
            # Replace this tile with an obstacle and re-walk the path
            self.patrol_map[pos] = self.patrol_map.BLOCKED
            try:
                self.patrol_map.walk_until_exit()
            except PatrolLoop:
                obstacles.add(pos)
            finally:
                # Return the map to it's prior state
                self.patrol_map[pos] = orig_val

        return len(obstacles)


if __name__ == '__main__':
    aoc = AOC2024Day6()
    aoc.run()
