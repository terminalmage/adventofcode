#!/usr/bin/env python
'''
https://adventofcode.com/2022/day/1
'''
# Local imports
from aoc import AOC


class AOC2022Day1(AOC):
    '''
    Day 1 of Advent of Code 2022
    '''
    def post_init(self) -> None:
        '''
        Calculate calories
        '''
        self.elf_calories: dict[int, int] = {}
        elf_number: int = 1
        calories: int = 0
        for line in self.input.splitlines():
            try:
                calories += int(line)
            except ValueError:
                # We've reached the blank line dividing groups of snacks.
                # Save the result, and then zero out the calorie count and
                # increment the elf number
                self.elf_calories[elf_number] = calories
                calories = 0
                elf_number += 1

            # When we get to the end of the file the exception above won't
            # trigger, so we need to save the last elf's calories.
            self.elf_calories[elf_number] = calories

    def part1(self) -> int:
        '''
        Calculate the top calorie count
        '''
        return max(self.elf_calories.values())

    def part2(self) -> int:
        '''
        Calculate the sum of the top three calorie counts
        '''
        return sum(sorted(self.elf_calories.values(), reverse=True)[:3])


if __name__ == '__main__':
    # Run against test data
    aoc = AOC2022Day1(example=True)
    aoc.validate(aoc.part1(), 24000)
    aoc.validate(aoc.part2(), 45000)
    # Run against actual data
    aoc = AOC2022Day1(example=False)
    aoc.run()
