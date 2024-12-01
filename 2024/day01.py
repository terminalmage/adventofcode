#!/usr/bin/env python
'''
https://adventofcode.com/2024/day/1
'''
import textwrap
from collections import Counter

# Local imports
from aoc import AOC


class AOC2024Day1(AOC):
    '''
    Day 1 of Advent of Code 2024
    '''
    example_data: str = textwrap.dedent(
        '''
        3   4
        4   3
        2   5
        1   3
        3   9
        3   3
        '''
    )

    validate_part1: int = 11
    validate_part2: int = 31

    # Set by post_init
    left = None
    right = None

    def post_init(self) -> None:
        '''
        Load the input data
        '''
        self.left: tuple[int, ...]
        self.right: tuple[int, ...]

        self.left, self.right = zip(
            *(map(int, row.split()) for row in self.input.splitlines())
        )

    def part1(self) -> int:
        '''
        Return the sum of differences, as defined in Part 1
        '''
        return sum(
            abs(x - y) for x, y in zip(
                sorted(self.left), sorted(self.right)
            )
        )

    def part2(self) -> int:
        '''
        Return the similarity score, as defined in Part 2
        '''
        counter: Counter = Counter(self.right)
        return sum(x * counter[x] for x in self.left)


if __name__ == '__main__':
    aoc = AOC2024Day1()
    aoc.run()
