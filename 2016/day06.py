#!/usr/bin/env python
'''
https://adventofcode.com/2016/day/6
'''
import collections

# Local imports
from aoc import AOC, Grid


class AOC2016Day6(AOC):
    '''
    Day 6 of Advent of Code 2016
    '''
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
    # Run against test data
    aoc = AOC2016Day6(example=True)
    aoc.validate(aoc.part1(), 'easter')
    aoc.validate(aoc.part2(), 'advent')
    # Run against actual data
    aoc = AOC2016Day6(example=False)
    aoc.run()
