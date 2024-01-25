#!/usr/bin/env python
'''
https://adventofcode.com/2017/day/14
'''
import textwrap
from collections.abc import Generator

# Local imports
from aoc import AOC, Grid, XY
from day10 import knot_hash

# Type hints
Region = set[XY]


class Disk(Grid):
    '''
    Grid object with modified neigbhors function to support flood fill
    '''
    def neighbors(
        self,
        coord: XY,
    ) -> Generator[XY, None, None]:
        '''
        Return neighboring coordinates which are '1' (i.e. used)
        '''
        in_grid = lambda r, c: 0 <= r <= self.max_row and 0 <= c <= self.max_col
        row, col = coord
        for (row_delta, col_delta) in self.directions:
            new_row, new_col = row + row_delta, col + col_delta
            if in_grid(new_row, new_col) and self.data[new_row][new_col] == '1':
                yield (new_row, new_col)

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
