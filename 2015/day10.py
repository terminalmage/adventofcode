#!/usr/bin/env python
'''
https://adventofcode.com/2015/day/10
'''
import re

# Local imports
from aoc import AOC


class AOC2015Day10(AOC):
    '''
    Day 10 of Advent of Code 2015
    '''
    day = 10

    def __init__(self, example: bool = False) -> None:
        '''
        Load the instructions
        '''
        super().__init__(example=example)
        self.sequence = self.input.read_text().strip()

    def look_and_say(self, rounds: int) -> str:
        '''
        Perform a depth-first search with the specified strategy
        '''
        seq = self.sequence

        for _ in range(rounds):
            parts = []
            for group in re.findall(r'([0-9])(\1*)', seq):
                parts.append(f'{len(group[1]) + 1}{group[0]}')
            seq = ''.join(parts)

        return seq

    def part1(self) -> int:
        '''
        Return length of string after 40 rounds
        '''
        return len(self.look_and_say(rounds=40))

    def part2(self) -> int:
        '''
        Return length of string after 50 rounds
        '''
        return len(self.look_and_say(rounds=50))


if __name__ == '__main__':
    # Run against test data
    aoc = AOC2015Day10(example=True)
    aoc.validate(aoc.part1(), 237746)
    aoc.validate(aoc.part2(), 3369156)
    # Run against actual data
    aoc = AOC2015Day10(example=False)
    aoc.run()
