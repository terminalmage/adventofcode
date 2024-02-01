#!/usr/bin/env python
'''
https://adventofcode.com/2018/day/2
'''
import itertools
import textwrap
from collections import Counter

# Local imports
from aoc import AOC


class AOC2018Day2(AOC):
    '''
    Day 2 of Advent of Code 2018
    '''
    example_data_part1: str = textwrap.dedent(
        '''
        abcdef
        bababc
        abbcde
        abcccd
        aabcdd
        abcdee
        ababab
        '''
    )

    example_data_part2: str = textwrap.dedent(
        '''
        abcde
        fghij
        klmno
        pqrst
        fguij
        axcye
        wvxyz
        '''
    )

    validate_part1: int = 12
    validate_part2: str = 'fgij'

    @staticmethod
    def matching_chars(box_id1: str, box_id2: str) -> list[str]:
        '''
        Return a list of the matching characters in the two box IDs
        '''
        c1: str
        c2: str
        return [
            c1 for c1, c2 in zip(box_id1, box_id2)
            if c1 == c2
        ]


    def part1(self) -> int:
        '''
        Return the number of strings that have at least one character that
        repeats exactly twice, multiplied by the number that have at least one
        character that repeats exactly three times.
        '''
        twos: int = 0
        threes: int = 0
        counts: set[int]
        for counts in (
            set(Counter(line).values())
            for line in self.input_part1.splitlines()
        ):
            if 2 in counts:
                twos += 1
            if 3 in counts:
                threes += 1

        return twos * threes

    def part2(self) -> str:
        '''
        Return the characters in common for the two boxes that only differ by a
        single character.
        '''
        lines: list[str] = self.input_part2.splitlines()
        target: int = len(lines[0]) - 1
        box_id1: str
        box_id2: str
        for box_id1, box_id2 in itertools.combinations(lines, 2):
            matching: list[str] = self.matching_chars(box_id1, box_id2)
            if len(matching) == target:
                return ''.join(matching)

        raise RuntimeError('Failed to find solution')


if __name__ == '__main__':
    aoc = AOC2018Day2()
    aoc.run()
