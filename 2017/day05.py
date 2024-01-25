#!/usr/bin/env python
'''
https://adventofcode.com/2017/day/5
'''
import textwrap

# Local imports
from aoc import AOC


class AOC2017Day5(AOC):
    '''
    Day 5 of Advent of Code 2017
    '''
    example_data: str = textwrap.dedent(
        '''
        0
        3
        0
        1
        -3
        '''
    )

    validate_part1: int = 5
    validate_part2: int = 10

    def post_init(self) -> None:
        '''
        Load the offsets from the input file
        '''
        self.offsets: tuple[int, ...] = tuple(
            int(line) for line in self.input.splitlines()
        )

    def part1(self) -> int:
        '''
        Follow and update the offsets until you exit the program
        '''
        offsets: list[int] = list(self.offsets)
        index: int = 0
        steps: int = 0

        while True:
            try:
                new_index: int = index + offsets[index]
            except IndexError:
                return steps
            offsets[index] += 1
            index = new_index
            steps += 1

    def part2(self) -> int:
        '''
        Follow and update the offsets until you exit the program
        '''
        offsets: list[int] = list(self.offsets)
        index: int = 0
        steps: int = 0

        while True:
            try:
                new_index: int = index + offsets[index]
            except IndexError:
                return steps
            if offsets[index] >= 3:
                offsets[index] -= 1
            else:
                offsets[index] += 1
            index = new_index
            steps += 1

if __name__ == '__main__':
    aoc = AOC2017Day5()
    aoc.run()
