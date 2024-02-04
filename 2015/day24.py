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
    # Set by post_init
    weights = None
    total_weight = None

    def post_init(self) -> None:
        '''
        Load the weight data
        '''
        self.weights: tuple[int, ...] = tuple(
            int(item) for item in self.input.splitlines()
        )
        self.total_weight = sum(self.weights)

    def solve(self, num_groups: int) -> int:
        '''
        Solve for the specified number of grouups
        '''
        target: int = self.total_weight // num_groups
        size: int
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
    aoc = AOC2015Day24()
    aoc.run()
