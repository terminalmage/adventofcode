#!/usr/bin/env python
'''
https://adventofcode.com/2017/day/17
'''
import textwrap
from collections import deque

# Local imports
from aoc import AOC

# Type hints
Buffer = deque[int]


class AOC2017Day17(AOC):
    '''
    Day 17 of Advent of Code 2017
    '''
    example_data: str = textwrap.dedent(
        '''
        3
        '''
    )

    validate_part1: int = 638

    # Set by post_init
    steps = None

    def post_init(self) -> None:
        '''
        Load the step length per round
        '''
        self.steps: int = int(self.input)

    def spinlock(self, rounds: int, target: int | None = None) -> Buffer:
        '''
        Initialize the Buffer and run the specified number of rounds. Once
        complete, find the index of target value and return the item that comes
        after it in the Buffer.
        '''
        if target is None:
            target = rounds

        buffer: Buffer = deque([0])

        for insertion in range(1, rounds + 1):
            buffer.rotate(-self.steps)
            buffer.append(insertion)

        return buffer[(buffer.index(target) + 1) % len(buffer)]

    def part1(self) -> int:
        '''
        Return the value after the last insertion, after 2017 insertions
        '''
        return self.spinlock(rounds=2017)

    def part2(self) -> int:
        '''
        Return the value after 0, after 50,000,000 insertions
        '''
        return self.spinlock(rounds=50_000_000, target=0)


if __name__ == '__main__':
    aoc = AOC2017Day17()
    aoc.run()
