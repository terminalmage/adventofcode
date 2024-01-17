#!/usr/bin/env python
'''
https://adventofcode.com/2017/day/4
'''
import collections
from collections.abc import Generator

# Local imports
from aoc import AOC


class AOC2017Day4(AOC):
    '''
    Day 4 of Advent of Code 2017
    '''
    day = 4

    def passphrases(self, part: int) -> Generator[str, None, None]:
        '''
        Generator that produces one passphrase at a time from the input
        '''
        with self.get_input(part=part).open() as fh:
            for line in fh:
                yield line.rstrip('\n')

    def part1(self) -> int:
        '''
        Return the number of valid passphrases using the criteria from Part 1
        '''
        return sum(
            collections.Counter(phrase.split()).most_common(1)[0][1] == 1
            for phrase in self.passphrases(part=1)
        )

    def part2(self) -> int:
        '''
        Return the number of valid passphrases using the criteria from Part 2
        '''
        return sum(
            collections.Counter(
                ''.join(sorted(word)) for word in phrase.split()
            ).most_common(1)[0][1] == 1
            for phrase in self.passphrases(part=2)
        )


if __name__ == '__main__':
    # Run against test data
    aoc = AOC2017Day4(example=True)
    aoc.validate(aoc.part1(), 2)
    aoc.validate(aoc.part2(), 3)
    # Run against actual data
    aoc = AOC2017Day4(example=False)
    aoc.run()
