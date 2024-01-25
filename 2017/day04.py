#!/usr/bin/env python
'''
https://adventofcode.com/2017/day/4
'''
import collections
import textwrap

# Local imports
from aoc import AOC


class AOC2017Day4(AOC):
    '''
    Day 4 of Advent of Code 2017
    '''
    example_data_part1: str = textwrap.dedent(
        '''
        aa bb cc dd ee
        aa bb cc dd aa
        aa bb cc dd aaa
        '''
    )

    example_data_part2: str = textwrap.dedent(
        '''
        abcde fghij
        abcde xyz ecdab
        a ab abc abd abf abj
        iiii oiii ooii oooi oooo
        oiii ioii iioi iiio
        '''
    )

    validate_part1: int = 2
    validate_part2: int = 3

    def part1(self) -> int:
        '''
        Return the number of valid passphrases using the criteria from Part 1
        '''
        return sum(
            collections.Counter(phrase.split()).most_common(1)[0][1] == 1
            for phrase in self.input_part1.splitlines()
        )

    def part2(self) -> int:
        '''
        Return the number of valid passphrases using the criteria from Part 2
        '''
        return sum(
            collections.Counter(
                ''.join(sorted(word)) for word in phrase.split()
            ).most_common(1)[0][1] == 1
            for phrase in self.input_part2.splitlines()
        )


if __name__ == '__main__':
    aoc = AOC2017Day4()
    aoc.run()
