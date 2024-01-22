#!/usr/bin/env python
'''
https://adventofcode.com/2017/day/14
'''
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
    day = 14

    def __init__(self, example: bool = False) -> None:
        '''
        Load the puzzle input
        '''
        super().__init__(example=example)
        self.key_string: str = self.input.read_text().strip()
        self.disk: Disk = Disk(
            bin(int(knot_hash(f'{self.key_string}-{i}'), 16))[2:].zfill(128)
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
    # Run against test data
    aoc = AOC2017Day14(example=True)
    aoc.validate(aoc.part1(), 8108)
    aoc.validate(aoc.part2(), 1242)
    # Run against actual data
    aoc = AOC2017Day14(example=False)
    aoc.run()
