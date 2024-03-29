#!/usr/bin/env python
'''
https://adventofcode.com/2015/day/10
'''
import re
import textwrap

# Local imports
from aoc import AOC


class AOC2015Day10(AOC):
    '''
    Day 10 of Advent of Code 2015
    '''
    example_data: str = textwrap.dedent(
        '''
        111221
        '''
    )

    validate_part1: int = 237746
    validate_part2: int = 3369156

    def look_and_say(self, rounds: int) -> str:
        '''
        Perform a depth-first search with the specified strategy
        '''
        seq: str = self.input

        for _ in range(rounds):
            parts = []
            group: str
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
    aoc = AOC2015Day10()
    aoc.run()
