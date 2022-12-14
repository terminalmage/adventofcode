#!/usr/bin/env python
'''
https://adventofcode.com/2022/day/18

--- Day 18: Boiling Boulders ---

You and the elephants finally reach fresh air. You've emerged near the base of
a large volcano that seems to be actively erupting! Fortunately, the lava seems
to be flowing away from you and toward the ocean.

Bits of lava are still being ejected toward you, so you're sheltering in the
cavern exit a little longer. Outside the cave, you can see the lava landing in
a pond and hear it loudly hissing as it solidifies.

Depending on the specific compounds in the lava and speed at which it cools, it
might be forming obsidian! The cooling rate should be based on the surface area
of the lava droplets, so you take a quick scan of a droplet as it flies past
you (your puzzle input).

Because of how quickly the lava is moving, the scan isn't very good; its
resolution is quite low and, as a result, it approximates the shape of the lava
droplet with 1x1x1 cubes on a 3D grid, each given as its x,y,z position.

To approximate the surface area, count the number of sides of each cube that
are not immediately connected to another cube. So, if your scan were only two
adjacent cubes like 1,1,1 and 2,1,1, each cube would have a single side covered
and five sides exposed, a total surface area of 10 sides.

Here's a larger example:

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

In the above example, after counting up all the sides that aren't connected to
another cube, the total surface area is 64.

What is the surface area of your scanned lava droplet?


--- Part Two ---

Something seems off about your calculation. The cooling rate depends on
exterior surface area, but your calculation also included the surface area of
air pockets trapped in the lava droplet.

Instead, consider only cube sides that could be reached by the water and steam
as the lava droplet tumbles into the pond. The steam will expand to reach as
much as possible, completely displacing any air on the outside of the lava
droplet but never expanding diagonally.

In the larger example above, exactly one cube of air is trapped within the lava
droplet (at 2,2,5), so the exterior surface area of the lava droplet is 58.

What is the exterior surface area of your scanned lava droplet?
'''
import collections
import functools
from collections.abc import Iterator

# Local imports
from aoc import AOC

# Typing shortcuts
Coordinate = tuple[int, int, int]


class AOC2022Day18(AOC):
    '''
    Day 18 of Advent of Code 2022
    '''
    day = 18

    def __init__(self, example: bool = False) -> None:
        '''
        Load the move list and translate it to coordinate deltas
        '''
        super().__init__(example=example)

        with self.input.open() as fh:
            self.droplet = frozenset(
                tuple(int(item) for item in line.rstrip().split(','))
                for line in fh
            )

        self.min_x = min(coord[0] for coord in self.droplet)
        self.max_x = max(coord[0] for coord in self.droplet)
        self.min_y = min(coord[1] for coord in self.droplet)
        self.max_y = max(coord[1] for coord in self.droplet)
        self.min_z = min(coord[2] for coord in self.droplet)
        self.max_z = max(coord[2] for coord in self.droplet)

    @staticmethod
    def adjacent(coord: Coordinate) -> Iterator[Coordinate]:
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
    def surface(self) -> Iterator[Coordinate]:
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
    def out_of_bounds(self, coord: Coordinate) -> bool:
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
    def is_edge(self, coord: Coordinate) -> bool:
        '''
        Return True if the coordinate is outside the droplet, otherwise False
        '''
        visited = {coord}
        dq = collections.deque(visited)

        # Perform a breadth-first search starting at the specified coordinate,
        # only adding to the queue if the neighboring node is not one of the
        # known coordinates that make up the droplet. Using this method, if we
        # reach an out-of-bounds coordinate, we know that we started our search
        # from the edge. The way we know this is that at least one of every
        # edge coordinate's neighbors will be out-of-bounds. Conversely, a
        # BFS started from a non-edge coordinate will never reach the edge, as
        # the search queue will run out of coordinates.
        while dq:
            coord = dq.popleft()
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
    # Run against test data
    aoc = AOC2022Day18(example=True)
    aoc.validate(aoc.part1(), 64)
    aoc.validate(aoc.part2(), 58)
    # Run against actual data
    aoc = AOC2022Day18(example=False)
    aoc.run()
