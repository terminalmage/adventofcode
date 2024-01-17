#!/usr/bin/env python
'''
https://adventofcode.com/2017/day/5
'''
# Local imports
from aoc import AOC


class AOC2017Day5(AOC):
    '''
    Day 5 of Advent of Code 2017
    '''
    day = 5

    def __init__(self, example: bool = False) -> None:
        '''
        Load the offsets from the input file
        '''
        super().__init__(example=example)
        self.offsets: tuple[int, ...] = tuple(
            int(line) for line in self.input.read_text().splitlines()
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
    # Run against test data
    aoc = AOC2017Day5(example=True)
    aoc.validate(aoc.part1(), 5)
    aoc.validate(aoc.part2(), 10)
    # Run against actual data
    aoc = AOC2017Day5(example=False)
    aoc.run()
