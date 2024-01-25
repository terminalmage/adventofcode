#!/usr/bin/env python
'''
https://adventofcode.com/2016/day/16
'''
import textwrap

# Local imports
from aoc import AOC


class AOC2016Day16(AOC):
    '''
    Day 16 of Advent of Code 2016
    '''
    example_data: str = textwrap.dedent(
        '''
        10000
        '''
    )

    validate_part1: str = '01100'

    def checksum(self, data: str):
        '''
        Calculate and return checksum of data
        '''
        checksum: str = ''
        index: int
        for index in range(0, len(data), 2):
            checksum += '1' if data[index] == data[index + 1] else '0'

        if len(checksum) % 2 == 0:
            # Valid checksums must be of odd length, if the length is even then
            # keep checksumming the checksums until we get an odd-length one.
            return self.checksum(checksum)

        return checksum

    def solve(self, data: str, size: int) -> str:
        '''
        Expand the initial data until it reaches the desired size, according to
        the algorithm described in the puzzle description, then return the
        checksum of that data.
        '''
        trans: dict[int, int] = str.maketrans('10', '01')

        while len(data) < size:
            data = f'{data}0{data[-1::-1].translate(trans)}'

        return self.checksum(data[:size])

    def part1(self) -> str:
        '''
        Expand the data until target size is reached, then return the checksum
        '''
        return self.solve(self.input, 20 if self.example else 272)

    def part2(self) -> str:
        '''
        Expand the data until target size is reached, then return the checksum
        '''
        return self.solve(self.input, 35651584)


if __name__ == '__main__':
    aoc = AOC2016Day16()
    aoc.run()
