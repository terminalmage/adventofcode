#!/usr/bin/env python
'''
https://adventofcode.com/2022/day/18
'''
import functools
import textwrap
from collections import deque
from collections.abc import Iterator

# Local imports
from aoc import AOC, XYZ


class AOC2022Day18(AOC):
    '''
    Day 18 of Advent of Code 2022
    '''
    example_data: str = textwrap.dedent(
        '''
        2,2,2
        1,2,2
        3,2,2
        2,1,2
        2,3,2
        2,2,1
        2,2,3
        2,2,4
        2,2,6
        1,2,5
        3,2,5
        2,1,5
        2,3,5
        '''
    )

    validate_part1: int = 64
    validate_part2: int = 58

    def post_init(self) -> None:
        '''
        Load the move list and translate it to coordinate deltas
        '''
        self.droplet: frozenset[XYZ] = frozenset(
            tuple(int(item) for item in line.split(','))
            for line in self.input.splitlines()
        )

        self.min_x: int = min(coord[0] for coord in self.droplet)
        self.max_x: int = max(coord[0] for coord in self.droplet)
        self.min_y: int = min(coord[1] for coord in self.droplet)
        self.max_y: int = max(coord[1] for coord in self.droplet)
        self.min_z: int = min(coord[2] for coord in self.droplet)
        self.max_z: int = max(coord[2] for coord in self.droplet)

    @staticmethod
    def adjacent(coord: XYZ) -> Iterator[XYZ]:
        '''
        Return a sequence of the x, y, z coordinates that are adjacent to the
        given coordinate
        '''
        yield (coord[0] - 1, coord[1], coord[2])
        yield (coord[0] + 1, coord[1], coord[2])
        yield (coord[0], coord[1] - 1, coord[2])
        yield (coord[0], coord[1] + 1, coord[2])
        yield (coord[0], coord[1], coord[2] - 1)
        yield (coord[0], coord[1], coord[2] + 1)

    @property
    def surface(self) -> Iterator[XYZ]:
        '''
        Generator function to return a sequence of x, y, z coordinates which
        are 1 unit away in each of the 3 axes, and which are also not part of
        the collection of coordinates that make up the lava droplet. These
        coordinates collectively represent the outside surface of the droplet.
        '''
        for coord in self.droplet:
            for adjacent in self.adjacent(coord):
                if adjacent not in self.droplet:
                    yield adjacent

    @functools.lru_cache
    def out_of_bounds(self, coord: XYZ) -> bool:
        '''
        Returns True if the coordinate is outside the min/max value on any
        of the 3 axes, otherwise False
        '''
        return not (
            self.min_x <= coord[0] <= self.max_x
            and self.min_y <= coord[1] <= self.max_y
            and self.min_z <= coord[2] <= self.max_z
        )

    @functools.lru_cache
    def is_edge(self, coord: XYZ) -> bool:
        '''
        Return True if the coordinate is outside the droplet, otherwise False
        '''
        visited = {coord}
        dq: deque[XYZ] = deque(visited)

        # Perform a breadth-first search starting at the specified coordinate,
        # only adding to the queue if the neighboring node is not one of the
        # known coordinates that make up the droplet. Using this method, if we
        # reach an out-of-bounds coordinate, we know that we started our search
        # from the edge. The way we know this is that at least one of every
        # edge coordinate's neighbors will be out-of-bounds. Conversely, a
        # BFS started from a non-edge coordinate will never reach the edge, as
        # the search queue will run out of coordinates.
        while dq:
            coord: XYZ = dq.popleft()
            adjacent: XYZ
            for adjacent in self.adjacent(coord):
                if adjacent not in visited:
                    if self.out_of_bounds(adjacent):
                        return True
                    if adjacent not in self.droplet:
                        visited.add(adjacent)
                        dq.append(adjacent)

        # Coordinate is not on the edge
        return False

    def part1(self) -> int:
        '''
        Calculate the surface area of all coordinates
        '''
        return sum(1 for coord in self.surface)

    def part2(self) -> int:
        '''
        Calculate the surface area of external coordinates only
        '''
        return sum(1 for coord in self.surface if self.is_edge(coord))


if __name__ == '__main__':
    aoc = AOC2022Day18()
    aoc.run()
