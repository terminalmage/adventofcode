#!/usr/bin/env python
'''
https://adventofcode.com/2015/day/4

--- Day 4: The Ideal Stocking Stuffer ---

Santa needs help mining some AdventCoins (very similar to bitcoins) to use as
gifts for all the economically forward-thinking little girls and boys.

To do this, he needs to find MD5 hashes which, in hexadecimal, start with at
least five zeroes. The input to the MD5 hash is some secret key (your puzzle
input, given below) followed by a number in decimal. To mine AdventCoins, you
must find Santa the lowest positive number (no leading zeroes: 1, 2, 3, ...)
that produces such a hash.

For example:

- If your secret key is abcdef, the answer is 609043, because the MD5 hash of
  abcdef609043 starts with five zeroes (000001dbbfa...), and it is the lowest
  such number to do so.

- If your secret key is pqrstuv, the lowest number it combines with to make an
  MD5 hash starting with five zeroes is 1048970; that is, the MD5 hash of
  pqrstuv1048970 looks like 000006136ef....

--- Part Two ---

Now find one that starts with six zeroes.
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
    day = 4

    def __init__(self, example: bool = False) -> None:
        '''
        Load the secret key
        '''
        super().__init__(example=example)
        self.secret_key = self.input.read_text().rstrip()

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
                hashlib.md5(f'{self.secret_key}{value}'.encode()).hexdigest(),
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
