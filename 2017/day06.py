#!/usr/bin/env python
'''
https://adventofcode.com/2017/day/6
'''
# Local imports
from aoc import AOC


class AOC2017Day6(AOC):
    '''
    Day 6 of Advent of Code 2017
    '''
    day = 6

    def __init__(self, example: bool = False) -> None:
        '''
        Set the target value depending on whether or not we are running with
        the example data.
        '''
        super().__init__(example=example)
        banks: list[int] = [
            int(bank) for bank in self.input.read_text().split()
        ]
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
    # Run against test data
    aoc = AOC2017Day6(example=True)
    aoc.validate(aoc.part1(), 5)
    aoc.validate(aoc.part2(), 4)
    # Run against actual data
    aoc = AOC2017Day6(example=False)
    aoc.run()
