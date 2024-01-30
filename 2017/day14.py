#!/usr/bin/env python
'''
https://adventofcode.com/2017/day/14
'''
import textwrap
from collections.abc import Iterator

# Local imports
from aoc import AOC, Grid, XY
from day10 import knot_hash

# Type hints
Region = set[XY]


class Disk(Grid):
    '''
    Grid object with modified neigbhors function to support flood fill
    '''
    def neighbors(self, coord: XY) -> Iterator[XY]:
        '''
        Return neighboring coordinates which are '1' (i.e. used)
        '''
        delta: XY
        for delta in self.directions:
            neighbor: XY = self.tuple_add(coord, delta)
            if neighbor in self and self[neighbor] == '1':
                yield neighbor

    @property
    def regions(self) -> list[set[XY], ...]:
        '''
        Return all the distinct regions of used space in the Disk
        '''
        used: set[XY] = {
            (row, col)
            for row in range(self.rows)
            for col in range(self.cols)
            if self[(row, col)] == '1'
        }

        def flood_fill(coord: XY, visited: Region | None = None) -> Region:
            '''
            Use the flood fill algorithm to find a continuous region containing
            the specified coordinate.
            '''
            visited = visited or set()

            if coord not in visited:
                visited.add(coord)
                neighbor: XY
                for neighbor in self.neighbors(coord):
                    flood_fill(neighbor, visited)

            return visited

        ret: list[Region] = []

        while used:
            ret.append(flood_fill(next(iter(used))))
            used -= ret[-1]

        return ret


class AOC2017Day14(AOC):
    '''
    Day 14 of Advent of Code 2017
    '''
    example_data: str = textwrap.dedent(
        '''
        flqrgnkx
        '''
    )

    validate_part1: int = 8108
    validate_part2: int = 1242

    def post_init(self) -> None:
        '''
        Load the puzzle input
        '''
        self.disk: Disk = Disk(
            bin(int(knot_hash(f'{self.input}-{i}'), 16))[2:].zfill(128)
            for i in range(128)
        )

    def part1(self) -> int:
        '''
        Return the number of used spaces in the Disk
        '''
        return sum(line.count('1') for line in self.disk)

    def part2(self) -> int:
        '''
        Return the number of distinct regions of used data in the Disk
        '''
        return len(self.disk.regions)


if __name__ == '__main__':
    aoc = AOC2017Day14()
    aoc.run()
