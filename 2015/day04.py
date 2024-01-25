#!/usr/bin/env python
'''
https://adventofcode.com/2015/day/4
'''
import hashlib
import itertools
import re

# Local imports
from aoc import AOC


class AOC2015Day4(AOC):
    '''
    Day 4 of Advent of Code 2015
    '''
    def coin_machine_go_brrr(  # pylint: disable=inconsistent-return-statements
        self,
        pattern: str,
    ) -> int:
        '''
        Return the lowest number that creates a hash matching the specified regex
        '''
        for value in itertools.count(1):
            if re.match(
                pattern,
                hashlib.md5(f'{self.input}{value}'.encode()).hexdigest(),
            ):
                return value

    def part1(self) -> int:
        '''
        Return the lowest number which produces a hash starting with 5 zeroes
        '''
        return self.coin_machine_go_brrr(r'^0{5,}')

    def part2(self) -> int:
        '''
        Return the lowest number which produces a hash starting with 6 zeroes
        '''
        return self.coin_machine_go_brrr(r'^0{6,}')


if __name__ == '__main__':
    # Run against test data
    aoc = AOC2015Day4(example=True)
    aoc.validate(aoc.part1(), 1048970)
    aoc.validate(aoc.part2(), 5714438)
    # Run against actual data
    aoc = AOC2015Day4(example=False)
    aoc.run()
