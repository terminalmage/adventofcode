#!/usr/bin/env python
'''
https://adventofcode.com/2015/day/2
'''
import functools

# Local imports
from aoc import AOC


class AOC2015Day2(AOC):
    '''
    Day 2 of Advent of Code 2015
    '''
    day = 2

    def __init__(self, example: bool = False) -> None:
        '''
        Load the packages, sorting the side lengths to easily get the two
        shortest sides
        '''
        super().__init__(example=example)
        with self.input.open() as fh:
            self.packages = tuple(
                item for item in (
                    tuple(
                        sorted(
                            int(side) for side in line.rstrip().split('x')
                        )
                    )
                    for line in fh
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
    # Run against test data
    aoc = AOC2015Day2(example=True)
    aoc.validate(aoc.part1(), 101)
    aoc.validate(aoc.part2(), 48)
    # Run against actual data
    aoc = AOC2015Day2(example=False)
    aoc.run()
