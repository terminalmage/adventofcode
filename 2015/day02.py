#!/usr/bin/env python
'''
https://adventofcode.com/2015/day/2
'''
import functools
import textwrap

# Local imports
from aoc import AOC


class AOC2015Day2(AOC):
    '''
    Day 2 of Advent of Code 2015
    '''
    example_data: str = textwrap.dedent(
        '''
        2x3x4
        1x1x10
        '''
    )

    validate_part1: int = 101
    validate_part2: int = 48

    # Set by post_init
    packages = None

    def post_init(self) -> None:
        '''
        Load the packages, sorting the side lengths to easily get the two
        shortest sides
        '''
        self.packages: tuple[tuple[int, ...], ...] = tuple(
            item for item in (
                tuple(
                    sorted(
                        int(side) for side in line.rstrip().split('x')
                    )
                )
                for line in self.input.splitlines()
            )
        )

    def part1(self) -> int:
        '''
        Return the amount of square feet of paper needed to wrap the packages
        '''
        return sum(
            (
                3 * (sides[0] * sides[1]) +
                2 * (sides[1] * sides[2]) +
                2 * (sides[0] * sides[2])
                for sides in self.packages
            )
        )

    def part2(self) -> int:
        '''
        Return the length of ribbon to make a bow for the packages
        '''
        return sum(
            (
                2 * (sides[0] + sides[1]) +
                functools.reduce(lambda x, y: x * y, sides)
                for sides in self.packages
            )
        )


if __name__ == '__main__':
    aoc = AOC2015Day2()
    aoc.run()
