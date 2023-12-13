#!/usr/bin/env python
'''
https://adventofcode.com/2015/day/24
'''
import itertools
import math

# Local imports
from aoc import AOC


class AOC2015Day24(AOC):
    '''
    Day 24 of Advent of Code 2015
    '''
    day = 24

    def __init__(self, example: bool = False) -> None:
        '''
        Load the input data
        '''
        super().__init__(example=example)
        self.weights = tuple(
            int(item) for item in self.input.read_text().splitlines()
        )
        self.total_weight = sum(self.weights)

    def solve(self, num_groups: int) -> int:
        '''
        Solve for the specified number of grouups
        '''
        target = self.total_weight // num_groups
        for size in range(1, len(self.weights) + 1):
            try:
                return min(
                    math.prod(group)
                    for group in itertools.combinations(self.weights, size)
                    if sum(group) == target
                )
            except ValueError:
                continue

    def part1(self) -> int:
        '''
        Solve for three groups
        '''
        return self.solve(3)

    def part2(self) -> int:
        '''
        Solve for four groups
        '''
        return self.solve(4)


if __name__ == '__main__':
    # Run against actual data
    aoc = AOC2015Day24(example=False)
    aoc.run()
