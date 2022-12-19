#!/usr/bin/env python
'''
https://adventofcode.com/2022/day/12
'''
from __future__ import annotations
import collections
import re
from collections.abc import Iterator, Sequence

# Local imports
from aoc2022 import AOC2022

# Typing shortcuts
Coordinate = tuple[int, int]


class AOC2022Day12(AOC2022):
    '''
    Day 12 of Advent of Code 2022
    '''
    day = 12

    def __init__(self, example: bool = False) -> None:
        '''
        Load the move list and translate it to coordinate deltas
        '''
        super().__init__(example=example)

        self.nodes = []
        valid = re.compile('^[a-zSE]+$')
        self.start = None
        self.end = None

        for row, line in enumerate(self.input.read_text().splitlines()):
            if not valid.match(line):
                raise ValueError(
                    f'Line #{row + 1} contains one or more invalid characters'
                )
            self.nodes.append([])
            for col, value in enumerate(line):
                coord = (row, col)
                if value == 'E':
                    if self.end is not None:
                        raise ValueError('More than one end point found')
                    self.end = coord
                    value = 'z'
                elif value == 'S':
                    if self.start is not None:
                        print(self.start)
                        raise ValueError('More than one start point found')
                    self.start = coord
                    value = 'a'

                # Assign an integer elevation for this coordinate. Lowercase
                # a-z letters have contiguous ordinal values, so ord(x) works
                # well as an elevation value.
                self.nodes[row].append(ord(value))

        self.num_rows = len(self.nodes)
        self.num_cols = len(self.nodes[0])

    def neighbors(self, row: int, col: int) -> Iterator[Coordinate]:
        '''
        Return all neighbors of the specified coordinate
        '''
        for neighbor_row, neighbor_col in (
            (row + 1, col),
            (row - 1, col),
            (row, col + 1),
            (row, col - 1),
        ):
            if (
                0 <= neighbor_row < self.num_rows and
                0 <= neighbor_col < self.num_cols
            ):
                # Make sure to only yield coordinates that are in bounds
                yield neighbor_row, neighbor_col

    def matches(self, char: int) -> Iterator[Coordinate]:
        '''
        Generator which returns all coordinates matching the specified
        character
        '''
        elevation = ord(char)
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                if self.nodes[row][col] == elevation:
                    yield row, col

    def bfs(self, *starting_points: Sequence[Coordinate]) -> int:
        '''
        Use breadth-first search to find distance of shortest path
        '''
        if not starting_points:
            raise ValueError('At least one start point is required')

        visited = set()

        dq = collections.deque((start, 0) for start in starting_points)

        while dq:
            coord, distance = dq.popleft()
            if coord == self.end:
                return distance

            elevation = self.nodes[coord[0]][coord[1]]
            for neighbor_coord in self.neighbors(*coord):
                row, col = neighbor_coord
                if (
                    1 >= (self.nodes[row][col] - elevation)
                    and neighbor_coord not in visited
                ):
                    visited.add(neighbor_coord)
                    dq.append((neighbor_coord, distance + 1))

    def part1(self) -> int:
        '''
        Calculate the fewest number of steps from start to end
        '''
        return self.bfs(aoc.start)

    def part2(self) -> int:
        '''
        Calculate the fewest number of steps from any starting point of
        elevation "a"
        '''
        return aoc.bfs(*aoc.matches('a'))


if __name__ == '__main__':
    # Run against test data
    aoc = AOC2022Day12(example=True)
    aoc.validate(aoc.part1(), 31)
    aoc.validate(aoc.part2(), 29)
    # Run against actual data
    aoc = AOC2022Day12(example=False)
    aoc.run()
