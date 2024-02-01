#!/usr/bin/env python
'''
https://adventofcode.com/2018/day/1
'''
import itertools
import textwrap

# Local imports
from aoc import AOC


class AOC2018Day1(AOC):
    '''
    Day 1 of Advent of Code 2018
    '''
    example_data: str = textwrap.dedent(
        '''
        +1
        -2
        +3
        +1
        '''
    )

    validate_part1: int = 3
    validate_part2: int = 2

    def post_init(self) -> None:
        '''
        Load the frequency deltas into a tuple
        '''
        self.deltas: tuple[int] = tuple(
            int(delta) for delta in self.input.splitlines()
        )

    def part1(self) -> int:
        '''
        Return the total change in frequency given the deltas from the input
        '''
        return sum(self.deltas)

    def part2(self) -> int:
        '''
        Return the first frequency seen twice
        '''
        freq: int = 0
        seen: set[int] = {freq}

        delta: int
        for delta in itertools.cycle(self.deltas):
            freq += delta
            if freq in seen:
                return freq
            seen.add(freq)


if __name__ == '__main__':
    aoc = AOC2018Day1()
    aoc.run()
