#!/usr/bin/env python
'''
https://adventofcode.com/2017/day/6
'''
import textwrap

# Local imports
from aoc import AOC


class AOC2017Day6(AOC):
    '''
    Day 6 of Advent of Code 2017
    '''
    example_data: str = textwrap.dedent(
        '''
        0 2 7 0
        '''
    )

    validate_part1: int = 5
    validate_part2: int = 4

    def post_init(self) -> None:
        '''
        Load the input data and simulate redistribution of the memory
        '''
        banks: list[int] = [int(bank) for bank in self.input.split()]
        self.cycles: int
        self.cycle_size: int
        self.cycles, self.cycle_size = self.redistribute(banks)

    @staticmethod
    def redistribute(banks: list[int]) -> tuple[int, int]:
        '''
        Run memory redistribution algorithm and return the number of cycles
        before loop is dectected, as well as the loop size.
        '''
        states: dict[tuple[int, ...], int] = {tuple(banks): 0}
        cycles: int = 0

        while True:
            cycles += 1
            # Find the rich
            pool: int = max(banks)
            index: int = banks.index(pool)
            # Eat the rich
            banks[index] = 0
            while pool:
                index = (index + 1) % len(banks)
                banks[index] += 1
                pool -= 1
            # Freeze state and detect loop
            state: tuple[int, ...] = tuple(banks)
            if state in states:
                return cycles, cycles - states[state]
            # Add state to known states
            states[state] = cycles

    def part1(self) -> int:
        '''
        Return number of cycles before a loop is detected
        '''
        return self.cycles

    def part2(self) -> int:
        '''
        Return cycle size
        '''
        return self.cycle_size


if __name__ == '__main__':
    aoc = AOC2017Day6()
    aoc.run()
