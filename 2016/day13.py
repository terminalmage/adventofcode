#!/usr/bin/env python
'''
https://adventofcode.com/2016/day/13
'''
from __future__ import annotations
import collections
import textwrap
from collections.abc import Iterator

# Local imports
from aoc import AOC, Coordinate, directions


class Tile(Coordinate):
    '''
    Subclass of Coordinate with modified logic for valid neighbors
    '''
    def neighbors(  # pylint: disable=arguments-differ,invalid-overridden-method
        self,
        favorite_number: int,
    ) -> Iterator[Tile]:
        '''
        Return the neighboring tiles which are open spaces. Negative values are
        invalid, so ignore any coordinate which would contain a negative value.
        '''
        for direction in directions:
            x: int = self.x + direction[0]
            y: int = self.y + direction[1]
            if x < 0 or y < 0:
                continue
            # Use the specified formula to calculate this tile's integer value
            result: int = x**2 + (3 * x) + (2 * x * y) + y + y**2 + favorite_number
            # If the number of bits that are 1 is even, this tile is an empty
            # space, yield it. Otherwise ignore it.
            if not bin(result).count('1') % 2:
                yield Tile(x, y)


class AOC2016Day13(AOC):
    '''
    Day 13 of Advent of Code 2016
    '''
    example_data: str = textwrap.dedent(
        '''
        10
        '''
    )

    validate_part1: int = 11

    def post_init(self) -> None:
        '''
        Set the favorite number as a class attribute
        '''
        self.favorite_number = int(self.input)

    def bfs(
        self,
        start: Tile = Tile(1, 1),
        dest: Tile | None = None,
        max_steps: int = 0,
    ) -> int:
        '''
        Find shortest number of steps to reach destination
        '''
        if dest is None and not max_steps:
            raise ValueError('A destination or max_steps must be provided')

        # Type hints
        Steps = int
        Key = tuple[Steps, Tile]
        steps: Steps
        tile: Tile

        dq: collections.deque[Key] = collections.deque([(0, start)])
        visited: set[Tile] = set()

        while dq:
            steps, tile = dq.popleft()

            if tile in visited:
                continue

            # If we've reached the destination, the first path in the BFS to
            # get to the destination will be the shortest, so return as soon as
            # we reach the destination.
            if dest and tile == dest:
                return steps

            # BFS will process all the tiles 1 step away before the tiles 2
            # steps away, all the 2-step tiles before 3-step tiles, etc.
            # Therefore, if the step count exceeds our max_steps, then we know
            # that visited contains the set of tiles that we can reach in
            # max_steps or fewer steps.
            if max_steps and steps > max_steps:
                return len(visited)

            visited.add(tile)

            steps += 1
            for neighbor in tile.neighbors(self.favorite_number):
                dq.append((steps, neighbor))

        # Shouldn't get here, but raise an exception rather than returning None
        raise RuntimeError('Queue empty before destination reached')

    def part1(self) -> int:
        '''
        Calculate the minimum steps to reach the destination
        '''
        return self.bfs(dest=Tile(7, 4) if self.example else Tile(31, 39))

    def part2(self) -> int:
        '''
        Calculate the number of distinct tiles that can be reached in 50 steps
        '''
        return self.bfs(max_steps=50)


if __name__ == '__main__':
    aoc = AOC2016Day13()
    aoc.run()
