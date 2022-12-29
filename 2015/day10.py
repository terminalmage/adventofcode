#!/usr/bin/env python
'''
https://adventofcode.com/2015/day/10

--- Day 10: Elves Look, Elves Say ---

Today, the Elves are playing a game called look-and-say. They take turns making
sequences by reading aloud the previous sequence and using that reading as the
next sequence. For example, 211 is read as "one two, two ones", which becomes
1221 (1 2, 2 1s).

Look-and-say sequences are generated iteratively, using the previous value as
input for the next step. For each step, take the previous value, and replace
each run of digits (like 111) with the number of digits (3) followed by the
digit itself (1).

For example:

- 1 becomes 11 (1 copy of digit 1).
- 11 becomes 21 (2 copies of digit 1).
- 21 becomes 1211 (one 2 followed by one 1).
- 1211 becomes 111221 (one 1, one 2, and two 1s).
- 111221 becomes 312211 (three 1s, two 2s, and one 1).

Starting with the digits in your puzzle input, apply this process 40 times.
What is the length of the result?

Your puzzle input is 3113322113.

--- Part Two ---

Now, starting again with the digits in your puzzle input, apply this process 50
times. What is the length of the new result?
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
