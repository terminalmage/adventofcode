#!/usr/bin/env python
'''
https://adventofcode.com/2015/day/1
'''
# Local imports
from aoc import AOC


class AOC2015Day1(AOC):
    '''
    Day 1 of Advent of Code 2015
    '''
    day = 1

    def __init__(self, example: bool = False) -> None:
        '''
        Load the instructions
        '''
        super().__init__(example=example)
        with self.input.open() as fh:
            self.instructions = fh.read().strip()

    def part1(self) -> int:
        '''
        Return the floor to which the instructions lead
        '''
        return self.instructions.count('(') - self.instructions.count(')')

    def part2(self) -> int:
        '''
        Return the position where the current floor goes negative
        '''
        floor = 0
        for index, position in enumerate(self.instructions, start=1):
            floor += 1 if position == '(' else -1
            if floor < 0:
                return index
        raise RuntimeError('Failed to find negative floor')


if __name__ == '__main__':
    # Run against test data
    aoc = AOC2015Day1(example=True)
    aoc.validate(aoc.part1(), 3)
    aoc.validate(aoc.part2(), 1)
    # Run against actual data
    aoc = AOC2015Day1(example=False)
    aoc.run()
