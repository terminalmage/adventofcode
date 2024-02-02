#!/usr/bin/env python
'''
https://adventofcode.com/2018/day/3
'''
import re
import textwrap
from collections import Counter, defaultdict
from collections.abc import Iterator

# Local imports
from aoc import AOC, XY


class AOC2018Day3(AOC):
    '''
    Day 3 of Advent of Code 2018
    '''
    example_data: str = textwrap.dedent(
        '''
        #1 @ 1,3: 4x4
        #2 @ 3,1: 4x4
        #3 @ 5,5: 2x2
        '''
    )

    validate_part1: int = 4
    validate_part2: str = 3

    @property
    def claims(self) -> Iterator[list[int]]:
        '''
        Yield claim information from puzzle input
        '''
        # Each line contains 5 numbers:
        #
        #   1. claim number
        #   2. row
        #   3. col
        #   4. width
        #   5. height
        #
        for line in self.input.splitlines():
            yield [int(i) for i in re.findall(r'\d+', line)]

    @staticmethod
    def expand(row: int, col: int, width: int, height: int) -> Iterator[XY]:
        '''
        Return all row/col pairs
        '''
        for x, y in (
            (r, c)
            for r in range(row, row + width)
            for c in range(col, col + height)
        ):
            yield x, y

    def part1(self) -> int:
        '''
        Return the number of coordinates that overlap
        '''
        swatches: dict[XY, int] = defaultdict(int)
        coord: XY
        for claim in self.claims:
            for coord in self.expand(*claim[1:]):
                swatches[coord] += 1

        return sum(
            count for occupants, count in Counter(swatches.values()).items()
            if occupants > 1
        )

    def part2(self) -> int:
        '''
        Return the non-overlapping claim
        '''
        swatches: dict[XY, set[int]] = defaultdict(set)
        claim_coords: dict[int, set[XY]] = defaultdict(set)
        coord: XY
        for claim in self.claims:
            for coord in self.expand(*claim[1:]):
                swatches[coord].add(claim[0])
                claim_coords[claim[0]].add(coord)

        claim_num: int
        for claim_num, coords in claim_coords.items():
            if all(len(swatches[coord]) == 1 for coord in coords):
                return claim_num

        raise RuntimeError('Failed to find non-overlapping claim')


if __name__ == '__main__':
    aoc = AOC2018Day3()
    aoc.run()
