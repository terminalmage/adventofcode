#!/usr/bin/env python
'''
https://adventofcode.com/2015/day/4
'''
import hashlib
import itertools
import re
import textwrap

# Local imports
from aoc import AOC


class AOC2015Day4(AOC):
    '''
    Day 4 of Advent of Code 2015
    '''
    example_data: str = textwrap.dedent(
        '''
        pqrstuv
        '''
    )

    validate_part1: int = 1048970
    validate_part2: int = 5714438

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
    aoc = AOC2015Day4()
    aoc.run()
