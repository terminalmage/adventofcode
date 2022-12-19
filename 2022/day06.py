#!/usr/bin/env python
'''
https://adventofcode.com/2022/day/6
'''
# Local imports
from aoc2022 import AOC2022


class AOC2022Day6(AOC2022):
    '''
    Day 6 of Advent of Code 2022
    '''
    day = 6

    def __init__(self, example: bool = False) -> None:
        '''
        Load the datastream
        '''
        super().__init__(example=example)
        self.datastream = self.input.read_text()

    def marker_index(self, length: int) -> int:
        '''
        Return the index of the marker
        '''
        for start in range(len(self.datastream) - length):
            if len(set(self.datastream[start:start + length])) == length:
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
    aoc = AOC2022Day6(example=True)
    aoc.validate(aoc.part1(), 7)
    aoc.validate(aoc.part2(), 19)
    # Run against actual data
    aoc = AOC2022Day6(example=False)
    aoc.run()
