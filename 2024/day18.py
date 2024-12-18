#!/usr/bin/env python
'''
https://adventofcode.com/2024/day/18
'''
import textwrap
from collections import deque
from typing import Literal

# Local imports
from aoc import AOC, TupleMixin, XY, directions

EMPTY: str = '.'
WALL: str = '#'

# Type hints
Tile = Literal[EMPTY, WALL]
MemorySpace = list[list[Tile]]


class TraversalError(Exception):
    '''
    Raise if BFS fails (i.e. no path to goal)
    '''


class AOC2024Day18(AOC, TupleMixin):
    '''
    Day 18 of Advent of Code 2024
    '''
    example_data: str = textwrap.dedent(
        '''
        5,4
        4,2
        4,5
        3,0
        2,1
        6,3
        2,4
        1,5
        0,6
        3,3
        2,6
        5,1
        1,2
        5,5
        2,5
        6,5
        1,4
        0,4
        6,4
        1,1
        6,1
        1,0
        0,5
        1,6
        2,0
        '''
    )

    validate_part1: int = 22
    validate_part2: str = '6,1'

    # Set by post_init
    obstructions = None
    size = None
    start = None
    goal = None
    nanoseconds = None

    def post_init(self) -> None:
        '''
        Set the size of the grid based on whether or not we are running against
        example data or actual puzzle input.
        '''
        # Load the puzzle input as an immutable sequence (i.e. tuple) of XY
        # coordinate pairs.
        self.obstructions: tuple[XY, ...] = tuple(
            tuple(map(int, line.split(',')))
            for line in self.input.splitlines()
        )
        # Grid size and time elapsed for Part 1 differ between example and
        # actual puzzle input.
        self.size: int = 7 if self.example else 71
        self.nanoseconds: int = 12 if self.example else 1024

        # The goal depends on the size of the grid
        self.goal: XY = 2 * (self.size - 1,)

        # We will always start at 0,0
        self.start: XY = (0, 0)

    def fewest_steps(self, nanoseconds: int):
        '''
        BFS solution to find the fewest steps needed to reach the goal, given
        that bytes have been falling for the specified number of nanoseconds.
        If there is no path to the goal, raise a TraversalError.
        '''
        # We start having walked 0 steps, at the position 0,0
        Steps = int
        dq: deque[tuple[Steps, XY]] = deque([(0, self.start)])

        # Track coordinates we have visited. Due to how BFS works (always
        # trying the next closest coordinate in all directions), we know that
        # if a later loop iteration reaches a given coordinate, it will not be
        # the fastest to reach that coordinate, and cannot possibly be part of
        # the optimal path to the goal.
        visited: set[XY] = set()

        # The obstruction locations will be different depending on how much
        # time has elapsed. They are stored as a tuple of coordinates, so the
        # set of obstructed coordinates after a specific number of nanoseconds
        # can be represented by a slice of that tuple. After N nanoseconds, the
        # slice below will represent the first N obstructions.
        obstructions: set[XY] = {*self.obstructions[:nanoseconds]}

        # BFS to find smallest number of steps to reach the goal. If there is
        # no path to the goal, the loop below will complete without returning
        # anything, and an exception will be raised.
        steps: Steps
        pos: XY
        while dq:
            steps, pos = dq.popleft()

            if pos == self.goal:
                # This is the first attempt to reach the goal, and therefore
                # the one to reach the goal in the fewest steps. Return the
                # number of steps taken.
                return steps

            if pos in visited:
                # Don't double back on coordinates we've already visited, they
                # will be guaranteed not to be part of the optimal path.
                continue
            visited.add(pos)

            # Attempt movement in every direction, ignoring coordinates outside
            # the bounds of the map and those blocked by an obstruction.
            delta: XY
            for delta in directions:
                new_pos: XY = self.tuple_add(pos, delta)
                # The all() expression here does bounds checking. Both the X
                # and Y axis are checked to ensure they fall within the bounds,
                # and all() will only return True if both are in bounds.
                if (
                    new_pos not in obstructions
                    and all(0 <= n <= (self.size - 1) for n in new_pos)
                ):
                    dq.append((steps + 1, new_pos))

        # No path to the goal
        raise TraversalError

    def part1(self) -> int:
        '''
        Return shortest number of steps to reach the bottom right of the grid,
        given the obstructions that have fallen after the specified number of
        nanoseconds. This amount is different for the example input than it is
        for the actual input, and so the number of nanoseconds has been set in
        the post_init() func above.
        '''
        return self.fewest_steps(self.nanoseconds)

    def part2(self) -> str:
        '''
        Use a binary search to find the first byte that will block the path
        '''
        low = self.nanoseconds
        high = len(self.obstructions) - 1

        while low <= high:
            # Select the midpoint between low and high
            middle: int = (low + high) // 2

            try:
                # Check to see if blocked. We don't care about the number of
                # steps returned, we only care if the BFS failed. So if our
                # custom exception class (TraversalError) got raised, the path
                # is blocked and the goal is unreachable.
                self.fewest_steps(middle)
            except TraversalError:
                # Path was blocked. In the next loop iteration, focus on the
                # items "lower" than the current one, keeping the lower bound.
                high = middle - 1
            else:
                # Path was not blocked. In the next loop iteration, focus on
                # the items "higher" than the current one, keeping the upper
                # bound.
                low = middle + 1

        # Once we complete the binary search, "high" is now the index of the
        # first obstruction to make the grid impossible to traverse. These
        # obstructions are stored as a tuple of ints though (the X and Y
        # coordinates of that obstruction), and the puzzle solution requires
        # that we express this as two ints with a comma between them. Convert
        # the items in the tuple to strings and then join them with a comma to
        # get the solution.
        return  ','.join(map(str, self.obstructions[high]))


if __name__ == '__main__':
    aoc = AOC2024Day18()
    aoc.run()
