#!/usr/bin/env python
'''
https://adventofcode.com/2022/day/6
'''
import textwrap

# Local imports
from aoc import AOC


class AOC2022Day6(AOC):
    '''
    Day 6 of Advent of Code 2022
    '''
    example_data: str = textwrap.dedent(
        '''
        mjqjpqmgbljsphdztnvjfqwrcgsmlb
        '''
    )

    validate_part1: int = 7
    validate_part2: int = 19

    def marker_index(self, length: int) -> int:
        '''
        Return the index of the marker
        '''
        start: int
        for start in range(len(self.input) - length):
            if len(set(self.input[start:start + length])) == length:
                return start

        raise ValueError(f'Invalid datastream for packet length: {length}')

    def packet_size(self, marker_length: int) -> int:
        '''
        Return the size of the packet, including the marker
        '''
        return self.marker_index(length=marker_length) + marker_length

    def part1(self) -> int:
        '''
        Calculate packet size
        '''
        return self.packet_size(marker_length=4)

    def part2(self) -> int:
        '''
        Calculate the size of the data before the first start-of-message marker
        '''
        return self.packet_size(marker_length=14)


if __name__ == '__main__':
    aoc = AOC2022Day6()
    aoc.run()
