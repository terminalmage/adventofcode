#!/usr/bin/env python
'''
https://adventofcode.com/2016/day/6
'''
import collections
import textwrap

# Local imports
from aoc import AOC, Grid


class AOC2016Day6(AOC):
    '''
    Day 6 of Advent of Code 2016
    '''
    example_data: str = textwrap.dedent(
        '''
        eedadn
        drvtee
        eandsr
        raavrd
        atevrs
        tsrnev
        sdttsa
        rasrtv
        nssdts
        ntnada
        svetve
        tesnvt
        vntsnd
        vrdear
        dvrsen
        enarar
        '''
    )

    validate_part1: str = 'easter'
    validate_part2: str = 'advent'

    def post_init(self) -> None:
        '''
        Load the Grid
        '''
        self.grid = Grid(self.input)

    def part1(self) -> str:
        '''
        Return the password using the method from Part 1
        '''
        return ''.join(
            collections.Counter(col).most_common(1)[0][0]
            for col in self.grid.column_iter()
        )

    def part2(self) -> str:
        '''
        Return the password using the method from Part 1
        '''
        return ''.join(
            collections.Counter(col).most_common()[-1][0]
            for col in self.grid.column_iter()
        )


if __name__ == '__main__':
    aoc = AOC2016Day6()
    aoc.run()
