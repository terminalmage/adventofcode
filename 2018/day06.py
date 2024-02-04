#!/usr/bin/env python
'''
https://adventofcode.com/2018/day/6
'''
import textwrap
from collections import Counter

# Local imports
from aoc import AOC, XYMixin, XY

# Type hints
Distances = dict[XY, int]


class AOC2018Day6(AOC, XYMixin):
    '''
    Day 6 of Advent of Code 2018
    '''
    example_data: str = textwrap.dedent(
        '''
        1, 1
        1, 6
        8, 3
        3, 4
        5, 5
        8, 9
        '''
    )

    validate_part1: int = 17
    validate_part2: int = 16

    # Set by post_init
    targets = None
    rows = None
    cols = None
    _distances = None
    closest_targets = None

    def post_init(self) -> None:
        '''
        Load the coordinates into a tuple of coordinate pairs
        '''
        # The coordinate pairs in this test are specified with col first then
        # row, while the functions in my XYMixin use row, col. Reverse the
        # coordinates in the puzzle input to make them work with my library.
        self.targets: frozenset[XY] = frozenset(
            tuple(reversed(tuple(int(n.strip()) for n in line.split(','))))
            for line in self.input.splitlines()
        )

        self.rows: int = max(n[0] for n in self.targets) + 1
        self.cols: int = max(n[1] for n in self.targets) + 1

        # memoization for distance lookups
        self._distances: dict[XY, Distances] = {}

        # Mapping of coordinates in the grid to the target closest to them, or
        # None if one or more target is tied for closest.
        self.closest_targets: dict[XY, XY | None] = {
            (x, y): self.closest((x, y))
            for x in range(self.rows)
            for y in range(self.cols)
        }

    def distances(self, coord: XY) -> Distances:
        '''
        Return the distance from the specified coordinate to each of the
        target coordinates from the puzzle input.
        '''
        if coord in self._distances:
            return self._distances[coord]

        self._distances[coord] = {
            target: self.distance(target, coord)
            for target in self.targets
        }
        return self._distances[coord]

    def closest(self, coord: XY) -> XY | None:
        '''
        Return the coordinate closest to the specified row and column. If
        there is a tie for the closest, then there is no one closest
        coordinate. In these cases, return None.
        '''
        # Get the distance from this coordinate for all of the coordinates in
        # our puzzle input
        distances: Distances = self.distances(coord)
        # Get the shortest distance, as well as how many times this distance
        # was seen
        distance: int
        frequency: int
        distance, frequency = min(Counter(distances.values()).items())
        # If the closest distance was seen more than once, then no one
        # coordinate from out puzzle input is closest. Therefore, return None.
        if frequency > 1:
            return None
        # Return the coordinate that matches our closest distance. We know that
        # there is only one, so next() can be used here instead of a for loop.
        return next(
            coord for coord, delta in distances.items()
            if delta == distance
        )

    def part1(self) -> int:
        '''
        Return the largest area which is not infinite
        '''
        # Gather all of our targets which are present on the edge of the grid.
        # Assume that these will extend out into infinity. Start by getting the
        # top row and bottom row.
        edge: set[XY] = {
            self.closest_targets[row, col]
            for row in (0, self.rows - 1)
            for col in range(self.cols)
        }
        # Add the first column in each row (excluding the first and last row
        # because we already did those), and do the same for the last column in
        # each row.
        edge.update({
            self.closest_targets[row, col]
            for row in range(1, self.rows - 1)
            for col in (0, self.cols - 1)
        })

        # Find the targets which are not on the edge. Coordinates which are on
        # the edge are assumed to extend out into infinity, making their area
        # infinite.
        not_infinite: frozenset[XY] = self.targets - edge

        # self.closest_targets contains a mapping of each coordinate in the
        # grid, to the target closest to it (or None if one or more are
        # closest). Therefore, using a Counter on the dict's values will give
        # us a Counter object mapping targets to their areas. Return the
        # largest area for a target which does not touch the edge of our grid.
        return max(
            area
            for target, area in Counter(self.closest_targets.values()).items()
            if target in not_infinite
        )

    def part2(self) -> int:
        '''
        Return the area of tiles for which the sum of the closest distances of
        all the targets is less than the limit.
        '''
        limit: int = 32 if self.example else 10_000
        return sum(
            sum(self.distances(coord).values()) < limit
            for coord in self.closest_targets
        )


if __name__ == '__main__':
    aoc = AOC2018Day6()
    aoc.run()
